"""Tests for client_type parameter passing to Dify service."""

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
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_default_client_type_is_web(mock_dify):
    """When no client_type is specified, it should default to 'web'."""
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

    mock_dify.assert_called_once()
    call_kwargs = mock_dify.call_args
    assert call_kwargs.kwargs.get("client_type") == "web" or \
           call_kwargs[1].get("client_type") == "web"


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_miniprogram_client_type_passed_to_dify(mock_dify):
    """When client_type='miniprogram', it should be forwarded to Dify."""
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/api/chat",
            json={"message": "hello", "client_type": "miniprogram"},
            headers={"Authorization": f"Bearer {token}"},
        )

    mock_dify.assert_called_once()
    call_kwargs = mock_dify.call_args
    assert call_kwargs.kwargs.get("client_type") == "miniprogram" or \
           call_kwargs[1].get("client_type") == "miniprogram"


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_custom_client_type_passed_through(mock_dify):
    """Arbitrary client_type values should be passed through to Dify."""
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/api/chat",
            json={"message": "hello", "client_type": "desktop"},
            headers={"Authorization": f"Bearer {token}"},
        )

    call_kwargs = mock_dify.call_args
    assert call_kwargs.kwargs.get("client_type") == "desktop" or \
           call_kwargs[1].get("client_type") == "desktop"
