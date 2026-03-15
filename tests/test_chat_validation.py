"""Tests for chat input validation and edge cases."""

import asyncio
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.auth import create_token


# ---------------------------------------------------------------------------
# Fake Dify stream
# ---------------------------------------------------------------------------

async def fake_dify_stream(query, user_id, conversation_id="", client_type="web"):
    yield {"event": "message", "answer": "ok", "conversation_id": "dify-1"}
    await asyncio.sleep(0)
    yield {"event": "workflow_finished", "conversation_id": "dify-1"}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_message_too_long_returns_400():
    """Messages exceeding MAX_MESSAGE_LENGTH (2000) should return 400."""
    from app.main import app

    token = create_token(1)
    long_message = "x" * 2001
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/chat",
            json={"message": long_message},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 400
    assert "2000" in resp.json()["detail"]


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_message_at_max_length_succeeds(mock_dify):
    """A message exactly at MAX_MESSAGE_LENGTH should succeed."""
    from app.main import app

    token = create_token(1)
    max_message = "x" * 2000
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/chat",
            json={"message": max_message},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_empty_message_body_returns_422():
    """Missing message field should return 422 (validation error)."""
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/chat",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 422


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_quota_deducted_even_on_dify_error(mock_dify_unused):
    """Quota is deducted BEFORE the Dify call, so even if Dify fails,
    quota is already consumed. This documents the known behavior."""
    from app.db.database import SessionLocal, User
    from app.main import app

    async def failing_dify_stream(query, user_id, conversation_id="", client_type="web"):
        raise ConnectionError("Dify is down")
        yield  # make it a generator  # noqa: unreachable

    token = create_token(1)
    with patch("app.api.chat.dify_service.send_message_stream", side_effect=failing_dify_stream):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            await client.post(
                "/api/chat",
                json={"message": "hello"},
                headers={"Authorization": f"Bearer {token}"},
            )

    # Quota was deducted even though Dify failed
    db = SessionLocal()
    user = db.query(User).filter(User.id == 1).first()
    assert user.free_quota == 9, "Quota should be deducted before Dify call"
    db.close()
