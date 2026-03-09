"""Tests for the auth API and JWT token handling."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.auth import create_token, verify_token


# ---------------------------------------------------------------------------
# JWT token tests
# ---------------------------------------------------------------------------


def test_create_and_verify_token():
    token = create_token(42)
    assert verify_token(token) == 42


def test_verify_expired_token():
    from datetime import datetime, timedelta

    import jwt

    from app.config import settings

    payload = {"user_id": 1, "exp": datetime.utcnow() - timedelta(days=1)}
    expired = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
    with pytest.raises(Exception) as exc_info:
        verify_token(expired)
    assert exc_info.value.status_code == 401
    assert "expired" in exc_info.value.detail.lower()


def test_verify_invalid_token():
    with pytest.raises(Exception) as exc_info:
        verify_token("garbage.token.value")
    assert exc_info.value.status_code == 401


# ---------------------------------------------------------------------------
# Login endpoint tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch(
    "app.services.wechat_service.code_to_session",
    new_callable=AsyncMock,
    return_value={"openid": "test-openid", "session_key": "sk"},
)
async def test_login_success(mock_wx):
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post("/api/login", json={"code": "mock-code"})

    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    assert data["remaining_quota"] == 10


@pytest.mark.asyncio
@patch(
    "app.services.wechat_service.code_to_session",
    new_callable=AsyncMock,
    return_value={"openid": "brand-new-user", "session_key": "sk"},
)
async def test_login_creates_new_user(mock_wx):
    from app.config import settings
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post("/api/login", json={"code": "mock-code"})

    assert resp.status_code == 200
    assert resp.json()["remaining_quota"] == settings.default_free_quota


@pytest.mark.asyncio
@patch(
    "app.services.wechat_service.code_to_session",
    new_callable=AsyncMock,
    side_effect=ValueError("WeChat login failed: invalid code"),
)
async def test_login_wechat_error(mock_wx):
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post("/api/login", json={"code": "bad-code"})

    assert resp.status_code == 400
    assert "WeChat" in resp.json()["detail"]


@pytest.mark.asyncio
@patch(
    "app.services.wechat_service.code_to_session",
    new_callable=AsyncMock,
    side_effect=ConnectionError("network down"),
)
async def test_login_unexpected_error_returns_502(mock_wx):
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post("/api/login", json={"code": "code"})

    assert resp.status_code == 502
    assert "WeChat API error" in resp.json()["detail"]


@pytest.mark.asyncio
@patch(
    "app.services.wechat_service.code_to_session",
    new_callable=AsyncMock,
    return_value={"session_key": "sk"},  # no openid
)
async def test_login_missing_openid_returns_502(mock_wx):
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post("/api/login", json={"code": "code"})

    assert resp.status_code == 502
    assert "no openid" in resp.json()["detail"]
