import json
import logging

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.api.auth import verify_token
from app.db.database import Conversation, Message, SessionLocal, User
from app.services import dify_service, quota_service

logger = logging.getLogger(__name__)

router = APIRouter()


MAX_MESSAGE_LENGTH = 2000


class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None
    client_type: str = "web"


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

        # Get or create conversation — always reuse the latest for this user.
        # 1. If client sends a conversation_id, try to use it
        # 2. Otherwise (or if not found), fall back to user's latest conversation
        # 3. Only create a new row if the user has zero conversations
        conv = None
        if req.conversation_id:
            conv = db.query(Conversation).filter(
                Conversation.id == req.conversation_id,
                Conversation.user_id == user_id,
            ).first()

        if not conv:
            conv = (
                db.query(Conversation)
                .filter(Conversation.user_id == user_id)
                .order_by(Conversation.id.desc())
                .first()
            )

        if not conv:
            user = db.query(User).filter(User.id == user_id).first()
            title = user.username or user.openid if user else str(user_id)
            conv = Conversation(user_id=user_id, title=title)
            db.add(conv)
            db.commit()
            db.refresh(conv)

        dify_conv_id = conv.dify_conversation_id or ""

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
        dify_conv_id_saved = False  # track whether we've persisted it

        try:
            async for event in dify_service.send_message_stream(
                query=req.message,
                user_id=str(user_id),
                conversation_id=dify_conv_id,
                client_type=req.client_type,
            ):
                event_type = event.get("event", "")

                # Capture and eagerly persist dify_conversation_id
                # so it survives even if the stream is interrupted.
                if event.get("conversation_id"):
                    dify_conv_id_from_stream = event["conversation_id"]
                    if not dify_conv_id_saved:
                        try:
                            eager_db = SessionLocal()
                            conv_obj = eager_db.query(Conversation).filter(
                                Conversation.id == conv_id_local
                            ).first()
                            if conv_obj and conv_obj.dify_conversation_id != dify_conv_id_from_stream:
                                conv_obj.dify_conversation_id = dify_conv_id_from_stream
                                eager_db.commit()
                            dify_conv_id_saved = True
                        except Exception:
                            logger.exception("Failed to eagerly save dify_conversation_id")
                        finally:
                            eager_db.close()

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
