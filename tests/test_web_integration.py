"""Integration tests: full web user flow (register → chat → restore conversation)."""

import asyncio
import json
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient


# ---------------------------------------------------------------------------
# Fake Dify stream generator
# ---------------------------------------------------------------------------

async def fake_dify_stream(query, user_id, conversation_id="", client_type="web"):
    yield {"event": "workflow_started", "conversation_id": "dify-web-conv"}
    await asyncio.sleep(0)
    yield {"event": "message", "answer": "Web reply!", "conversation_id": "dify-web-conv"}
    await asyncio.sleep(0)
    yield {"event": "workflow_finished", "conversation_id": "dify-web-conv"}


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
# Full flow tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_web_user_full_flow(mock_dify):
    """Register → chat → restore conversation → check quota."""
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # 1. Register
        reg_resp = await client.post(
            "/api/web/register",
            json={"username": "flowuser", "password": "pass1234"},
        )
        assert reg_resp.status_code == 200
        token = reg_resp.json()["token"]
        initial_quota = reg_resp.json()["remaining_quota"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Send a chat message
        chat_resp = await client.post(
            "/api/chat",
            json={"message": "How do I install OpenClaw?"},
            headers=headers,
        )
        assert chat_resp.status_code == 200
        events = parse_sse_events(chat_resp.text)

        msg_events = [e for e in events if e["type"] == "message"]
        done_events = [e for e in events if e["type"] == "done"]
        assert len(msg_events) >= 1
        assert len(done_events) == 1
        assert msg_events[0]["content"] == "Web reply!"

        conv_id = done_events[0]["conversation_id"]

        # 3. Restore conversation
        latest_resp = await client.get(
            "/api/conversation/latest", headers=headers
        )
        assert latest_resp.status_code == 200
        data = latest_resp.json()
        assert data["conversation_id"] == conv_id
        assert len(data["messages"]) == 2
        assert data["messages"][0]["role"] == "user"
        assert data["messages"][1]["role"] == "assistant"
        assert data["messages"][1]["content"] == "Web reply!"

        # 4. Check quota decreased
        quota_resp = await client.get("/api/quota", headers=headers)
        assert quota_resp.status_code == 200
        assert quota_resp.json()["remaining"] == initial_quota - 1


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_web_user_second_message_in_conversation(mock_dify):
    """Web user can send multiple messages in the same conversation."""
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        reg_resp = await client.post(
            "/api/web/register",
            json={"username": "multiuser", "password": "pass1234"},
        )
        token = reg_resp.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # First message
        resp1 = await client.post(
            "/api/chat",
            json={"message": "first"},
            headers=headers,
        )
        events1 = parse_sse_events(resp1.text)
        conv_id = [e for e in events1 if e["type"] == "done"][0]["conversation_id"]

        # Second message in same conversation
        resp2 = await client.post(
            "/api/chat",
            json={"message": "second", "conversation_id": conv_id},
            headers=headers,
        )
        assert resp2.status_code == 200
        events2 = parse_sse_events(resp2.text)
        done2 = [e for e in events2 if e["type"] == "done"]
        assert len(done2) == 1

        # Conversation should have 4 messages (2 user + 2 assistant)
        latest_resp = await client.get(
            "/api/conversation/latest", headers=headers
        )
        assert len(latest_resp.json()["messages"]) == 4


@pytest.mark.asyncio
async def test_web_user_401_without_token():
    """API endpoints should return 401 for unauthenticated web requests."""
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get(
            "/api/conversation/latest",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_web_users_isolated():
    """Two web users should not see each other's conversations."""
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Register two users
        r1 = await client.post(
            "/api/web/register",
            json={"username": "user_a", "password": "pass1234"},
        )
        r2 = await client.post(
            "/api/web/register",
            json={"username": "user_b", "password": "pass1234"},
        )
        token_a = r1.json()["token"]
        token_b = r2.json()["token"]

        # User A has no conversations
        resp_a = await client.get(
            "/api/conversation/latest",
            headers={"Authorization": f"Bearer {token_a}"},
        )
        assert resp_a.json()["conversation_id"] is None

        # User B also has no conversations
        resp_b = await client.get(
            "/api/conversation/latest",
            headers={"Authorization": f"Bearer {token_b}"},
        )
        assert resp_b.json()["conversation_id"] is None


@pytest.mark.asyncio
async def test_login_then_use_api():
    """Login (not register) and use the token to access an API endpoint."""
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Register
        await client.post(
            "/api/web/register",
            json={"username": "apiuser", "password": "pass1234"},
        )
        # Login
        login_resp = await client.post(
            "/api/web/login",
            json={"username": "apiuser", "password": "pass1234"},
        )
        token = login_resp.json()["token"]

        # Use token to hit quota endpoint
        quota_resp = await client.get(
            "/api/quota",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert quota_resp.status_code == 200
        assert quota_resp.json()["remaining"] > 0
