"""Extended tests for the chat endpoint covering quota exhaustion,
conversation not found, auth edge cases, and stream error handling."""

import asyncio
import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.auth import create_token


# ---------------------------------------------------------------------------
# Fake Dify generators
# ---------------------------------------------------------------------------

async def fake_dify_stream(query, user_id, conversation_id="", client_type="web"):
    yield {"event": "message", "answer": "reply", "conversation_id": "dify-123"}
    await asyncio.sleep(0)
    yield {"event": "workflow_finished", "conversation_id": "dify-123"}


async def fake_dify_stream_error(query, user_id, conversation_id="", client_type="web"):
    yield {"event": "message", "answer": "partial", "conversation_id": "dify-123"}
    await asyncio.sleep(0)
    raise ConnectionError("Dify API connection lost")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_chat_returns_403_when_quota_exhausted(mock_dify):
    """POST /api/chat should return 403 when user has no quota remaining."""
    from app.db.database import SessionLocal, User
    from app.main import app

    # Zero out quota
    db = SessionLocal()
    user = db.query(User).filter(User.id == 1).first()
    user.free_quota = 0
    user.paid_quota = 0
    db.commit()
    db.close()

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/chat",
            json={"message": "hello"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 403
    assert "对话次数已用完" in resp.json()["detail"]
    mock_dify.assert_not_called()


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_chat_falls_back_when_conversation_not_found(mock_dify):
    """POST /api/chat with a non-existent conversation_id should fall back
    to the user's latest conversation (or create one), not return 404."""
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/chat",
            json={"message": "hello", "conversation_id": 99999},
            headers={"Authorization": f"Bearer {token}"},
        )

    # Should succeed (falls back to creating a new conversation)
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_chat_returns_401_for_invalid_token():
    """POST /api/chat with a bad token should return 401."""
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/chat",
            json={"message": "hello"},
            headers={"Authorization": "Bearer invalid-token"},
        )

    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_chat_returns_422_without_auth_header():
    """POST /api/chat without Authorization header should return 422."""
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post("/api/chat", json={"message": "hello"})

    assert resp.status_code == 422


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream_error)
async def test_chat_stream_error_yields_error_event(mock_dify):
    """When Dify stream raises an exception, client should get an error SSE event."""
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/chat",
            json={"message": "hello"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200  # SSE always returns 200
    events = []
    for line in resp.text.split("\n"):
        line = line.strip()
        if line.startswith("data: "):
            try:
                events.append(json.loads(line[6:]))
            except json.JSONDecodeError:
                pass

    error_events = [e for e in events if e.get("type") == "error"]
    assert len(error_events) == 1
    assert "connection lost" in error_events[0]["content"].lower()


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_chat_deducts_quota(mock_dify):
    """A successful chat message should deduct 1 from the user's quota."""
    from app.db.database import SessionLocal, User
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/api/chat",
            json={"message": "hello"},
            headers={"Authorization": f"Bearer {token}"},
        )

    db = SessionLocal()
    user = db.query(User).filter(User.id == 1).first()
    assert user.free_quota == 9  # started at 10
    db.close()


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_chat_saves_messages_to_db(mock_dify):
    """After a chat, both user and assistant messages should be in the DB."""
    from app.db.database import Conversation, Message, SessionLocal
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/api/chat",
            json={"message": "test question"},
            headers={"Authorization": f"Bearer {token}"},
        )

    db = SessionLocal()
    conv = db.query(Conversation).filter(Conversation.user_id == 1).first()
    assert conv is not None
    assert conv.dify_conversation_id == "dify-123"

    messages = db.query(Message).filter(Message.conversation_id == conv.id).order_by(Message.id).all()
    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[0].content == "test question"
    assert messages[1].role == "assistant"
    assert messages[1].content == "reply"
    db.close()
