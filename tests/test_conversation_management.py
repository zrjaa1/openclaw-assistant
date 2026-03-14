"""Tests for conversation management: deduplication, title setting,
and reuse behavior that prevent regressions from past bugs."""

import asyncio
import json
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.auth import create_token


# ---------------------------------------------------------------------------
# Fake Dify stream
# ---------------------------------------------------------------------------

async def fake_dify_stream(query, user_id, conversation_id="", client_type="web"):
    yield {"event": "message", "answer": "reply", "conversation_id": "dify-abc"}
    await asyncio.sleep(0)
    yield {"event": "workflow_finished", "conversation_id": "dify-abc"}


def parse_sse_events(body: str) -> list[dict]:
    events = []
    for line in body.split("\n"):
        line = line.strip()
        if line.startswith("data: "):
            try:
                events.append(json.loads(line[6:]))
            except json.JSONDecodeError:
                pass
    return events


# ---------------------------------------------------------------------------
# Conversation deduplication (regression test for duplicate rows bug)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_multiple_messages_reuse_single_conversation(mock_dify):
    """Sending multiple messages should reuse the same conversation row,
    not create a new one each time. This is a regression test for the
    duplicate conversation bug."""
    from app.db.database import Conversation, SessionLocal
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Send 3 messages without specifying conversation_id
        for i in range(3):
            resp = await client.post(
                "/api/chat",
                json={"message": f"message {i}"},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert resp.status_code == 200

    db = SessionLocal()
    convs = db.query(Conversation).filter(Conversation.user_id == 1).all()
    assert len(convs) == 1, f"Expected 1 conversation, got {len(convs)}"
    db.close()


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_conversation_id_reuses_existing(mock_dify):
    """When client sends a conversation_id, the server should reuse
    that conversation rather than creating a new one."""
    from app.db.database import Conversation, Message, SessionLocal
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # First message creates a conversation
        resp1 = await client.post(
            "/api/chat",
            json={"message": "first"},
            headers={"Authorization": f"Bearer {token}"},
        )
        events1 = parse_sse_events(resp1.text)
        conv_id = [e for e in events1 if e.get("type") == "done"][0]["conversation_id"]

        # Second message explicitly references that conversation
        resp2 = await client.post(
            "/api/chat",
            json={"message": "second", "conversation_id": conv_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp2.status_code == 200

    db = SessionLocal()
    convs = db.query(Conversation).filter(Conversation.user_id == 1).all()
    assert len(convs) == 1

    messages = db.query(Message).filter(Message.conversation_id == conv_id).all()
    assert len(messages) == 4  # 2 user + 2 assistant
    db.close()


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_wrong_conversation_id_falls_back_to_latest(mock_dify):
    """A conversation_id belonging to another user should fall back
    to the current user's latest conversation, not create duplicates."""
    from app.db.database import Conversation, SessionLocal, User
    from app.main import app

    # Create a second user with their own conversation
    db = SessionLocal()
    user2 = User(openid="other-user", free_quota=10)
    db.add(user2)
    db.commit()
    other_conv = Conversation(user_id=user2.id, title="other")
    db.add(other_conv)
    db.commit()
    other_conv_id = other_conv.id
    db.close()

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # First message to create user 1's conversation
        await client.post(
            "/api/chat",
            json={"message": "setup"},
            headers={"Authorization": f"Bearer {token}"},
        )

        # Try to use user 2's conversation_id
        resp = await client.post(
            "/api/chat",
            json={"message": "sneaky", "conversation_id": other_conv_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200

    db = SessionLocal()
    user1_convs = db.query(Conversation).filter(Conversation.user_id == 1).all()
    assert len(user1_convs) == 1, "Should reuse existing, not create a new one"
    db.close()


# ---------------------------------------------------------------------------
# Conversation title
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_new_conversation_title_uses_openid(mock_dify):
    """When a WeChat user (no username) creates a conversation,
    the title should be set to their openid."""
    from app.db.database import Conversation, SessionLocal
    from app.main import app

    token = create_token(1)  # user has openid="test-openid", no username
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/api/chat",
            json={"message": "hello"},
            headers={"Authorization": f"Bearer {token}"},
        )

    db = SessionLocal()
    conv = db.query(Conversation).filter(Conversation.user_id == 1).first()
    assert conv.title == "test-openid"
    db.close()


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_new_conversation_title_uses_username_for_web_user(mock_dify):
    """When a web user (with username) creates a conversation,
    the title should be set to their username."""
    from app.db.database import Conversation, SessionLocal, User
    from app.main import app

    # Set up a web user with a username
    db = SessionLocal()
    web_user = User(openid="web:alice", username="alice", free_quota=10)
    db.add(web_user)
    db.commit()
    web_user_id = web_user.id
    db.close()

    token = create_token(web_user_id)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/api/chat",
            json={"message": "hello"},
            headers={"Authorization": f"Bearer {token}"},
        )

    db = SessionLocal()
    conv = db.query(Conversation).filter(Conversation.user_id == web_user_id).first()
    assert conv.title == "alice"
    db.close()
