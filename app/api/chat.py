import json
import logging

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.api.auth import verify_token
from app.db.database import Conversation, Message, SessionLocal
from app.services import dify_service, quota_service

logger = logging.getLogger(__name__)

router = APIRouter()


MAX_MESSAGE_LENGTH = 2000


class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None


class MessageOut(BaseModel):
    role: str
    content: str


class ConversationOut(BaseModel):
    conversation_id: int
    messages: list[MessageOut]


@router.get("/api/conversation/latest")
async def get_latest_conversation(authorization: str = Header(...)):
    """Return the user's most recent conversation with message history."""
    token = authorization.removeprefix("Bearer ").strip()
    user_id = verify_token(token)

    db = SessionLocal()
    try:
        conv = (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.id.desc())
            .first()
        )
        if not conv:
            return {"conversation_id": None, "messages": []}

        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conv.id)
            .order_by(Message.id.asc())
            .all()
        )
        return ConversationOut(
            conversation_id=conv.id,
            messages=[MessageOut(role=m.role, content=m.content) for m in messages],
        )
    finally:
        db.close()


@router.post("/api/chat")
async def chat(req: ChatRequest, authorization: str = Header(...)):
    token = authorization.removeprefix("Bearer ").strip()
    user_id = verify_token(token)

    if len(req.message) > MAX_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"消息长度不能超过{MAX_MESSAGE_LENGTH}字。",
        )

    db = SessionLocal()
    try:
        # Check quota
        if not quota_service.check_and_deduct(db, user_id):
            raise HTTPException(
                status_code=403,
                detail="对话次数已用完，请充值后继续使用。",
            )

        # Get or create conversation
        if req.conversation_id:
            conv = db.query(Conversation).filter(
                Conversation.id == req.conversation_id,
                Conversation.user_id == user_id,
            ).first()
            if not conv:
                raise HTTPException(status_code=404, detail="Conversation not found")
            dify_conv_id = conv.dify_conversation_id
        else:
            conv = Conversation(user_id=user_id)
            db.add(conv)
            db.commit()
            db.refresh(conv)
            dify_conv_id = ""

        # Save user message
        user_msg = Message(
            conversation_id=conv.id,
            role="user",
            content=req.message,
        )
        db.add(user_msg)
        db.commit()

        conv_id_local = conv.id
    finally:
        db.close()

    async def event_stream():
        full_answer = ""
        dify_conv_id_from_stream = ""

        try:
            async for event in dify_service.send_message_stream(
                query=req.message,
                user_id=str(user_id),
                conversation_id=dify_conv_id,
            ):
                event_type = event.get("event", "")

                # Capture conversation_id from any event that has it
                if event.get("conversation_id"):
                    dify_conv_id_from_stream = event["conversation_id"]

                if event_type == "message":
                    chunk = event.get("answer", "")
                    if chunk:
                        full_answer += chunk
                        yield f"data: {json.dumps({'type': 'message', 'content': chunk}, ensure_ascii=False)}\n\n"

                elif event_type in ("message_end", "workflow_finished"):
                    logger.info(
                        "%s: local_conv=%s, dify_conv=%s",
                        event_type, conv_id_local, dify_conv_id_from_stream,
                    )

                    # Save BEFORE yielding done — once we yield,
                    # the cloud proxy may close the connection and
                    # the generator cleanup code won't run.
                    save_db = SessionLocal()
                    try:
                        assistant_msg = Message(
                            conversation_id=conv_id_local,
                            role="assistant",
                            content=full_answer,
                        )
                        save_db.add(assistant_msg)

                        if dify_conv_id_from_stream:
                            conv_obj = save_db.query(Conversation).filter(
                                Conversation.id == conv_id_local
                            ).first()
                            if conv_obj:
                                conv_obj.dify_conversation_id = dify_conv_id_from_stream

                        save_db.commit()
                    finally:
                        save_db.close()

                    yield f"data: {json.dumps({'type': 'done', 'conversation_id': conv_id_local}, ensure_ascii=False)}\n\n"

        except Exception as e:
            logger.exception("Error in chat stream")
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
