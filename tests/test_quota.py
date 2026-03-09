"""Tests for quota service and API endpoint."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.auth import create_token
from app.db.database import SessionLocal, User
from app.services.quota_service import check_and_deduct, get_remaining


# ---------------------------------------------------------------------------
# Quota service unit tests
# ---------------------------------------------------------------------------


def test_get_remaining(db):
    assert get_remaining(db, user_id=1) == 10


def test_get_remaining_nonexistent_user(db):
    assert get_remaining(db, user_id=999) == 0


def test_check_and_deduct_free_quota(db):
    assert check_and_deduct(db, user_id=1) is True
    assert get_remaining(db, user_id=1) == 9


def test_check_and_deduct_paid_quota(db):
    user = db.query(User).filter(User.id == 1).first()
    user.free_quota = 0
    user.paid_quota = 5
    db.commit()

    assert check_and_deduct(db, user_id=1) is True
    db.refresh(user)
    assert user.paid_quota == 4
    assert user.free_quota == 0


def test_check_and_deduct_prefers_free_over_paid(db):
    user = db.query(User).filter(User.id == 1).first()
    user.free_quota = 2
    user.paid_quota = 3
    db.commit()

    assert check_and_deduct(db, user_id=1) is True
    db.refresh(user)
    assert user.free_quota == 1
    assert user.paid_quota == 3  # untouched


def test_check_and_deduct_no_quota(db):
    user = db.query(User).filter(User.id == 1).first()
    user.free_quota = 0
    user.paid_quota = 0
    db.commit()

    assert check_and_deduct(db, user_id=1) is False


def test_check_and_deduct_nonexistent_user(db):
    assert check_and_deduct(db, user_id=999) is False


# ---------------------------------------------------------------------------
# Quota API endpoint tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_quota_endpoint(token):
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get(
            "/api/quota", headers={"Authorization": f"Bearer {token}"}
        )

    assert resp.status_code == 200
    assert resp.json()["remaining"] == 10


@pytest.mark.asyncio
async def test_quota_endpoint_no_auth():
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/quota")

    assert resp.status_code == 422  # missing header


@pytest.mark.asyncio
async def test_quota_endpoint_invalid_token():
    from app.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get(
            "/api/quota", headers={"Authorization": "Bearer bad-token"}
        )

    assert resp.status_code == 401
