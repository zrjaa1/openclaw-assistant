"""Tests for the web auth endpoints (register + login)."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.auth import verify_token


# ---------------------------------------------------------------------------
# Register tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_register_success():
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/web/register",
            json={"username": "newuser", "password": "secret123"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    assert data["remaining_quota"] > 0
    # Token should be valid
    user_id = verify_token(data["token"])
    assert user_id is not None


@pytest.mark.asyncio
async def test_register_duplicate_username():
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/api/web/register",
            json={"username": "dupuser", "password": "secret123"},
        )
        resp = await client.post(
            "/api/web/register",
            json={"username": "dupuser", "password": "other456"},
        )

    assert resp.status_code == 409
    # English default (no Accept-Language header)
    assert "already taken" in resp.json()["detail"].lower() or "已被注册" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_register_username_too_short():
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/web/register",
            json={"username": "ab", "password": "secret123"},
        )

    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_username_too_long():
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/web/register",
            json={"username": "a" * 33, "password": "secret123"},
        )

    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_password_too_short():
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/web/register",
            json={"username": "validuser", "password": "12345"},
        )

    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_missing_fields():
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post("/api/web/register", json={})

    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Login tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_login_success():
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Register first
        await client.post(
            "/api/web/register",
            json={"username": "loginuser", "password": "secret123"},
        )
        # Then login
        resp = await client.post(
            "/api/web/login",
            json={"username": "loginuser", "password": "secret123"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    assert data["remaining_quota"] > 0


@pytest.mark.asyncio
async def test_login_wrong_password():
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/api/web/register",
            json={"username": "wrongpw", "password": "secret123"},
        )
        resp = await client.post(
            "/api/web/login",
            json={"username": "wrongpw", "password": "wrongpass"},
        )

    assert resp.status_code == 401
    detail = resp.json()["detail"].lower()
    assert "invalid" in detail or "密码错误" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_login_nonexistent_user():
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/web/login",
            json={"username": "noexist", "password": "whatever"},
        )

    assert resp.status_code == 401
    detail = resp.json()["detail"].lower()
    assert "invalid" in detail or "密码错误" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_login_wechat_user_cannot_web_login():
    """WeChat users (no password_hash) should not be able to log in via web."""
    from app.main import app

    # The conftest creates a user with openid="test-openid" but no password_hash.
    # Try logging in with that user's openid as username — should fail.
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/web/login",
            json={"username": "test-openid", "password": "anything"},
        )

    assert resp.status_code == 401
