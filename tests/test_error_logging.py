"""Tests for centralized error logging in the HTTP exception handler."""

import logging

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.auth import create_token


@pytest.mark.asyncio
async def test_401_logs_user_info():
    """401 errors should log the user identity (invalid-token for bad tokens)."""
    from app.main import app

    records = []

    class CapturingHandler(logging.Handler):
        def emit(self, record):
            records.append(record)

    logger = logging.getLogger("app.main")
    handler = CapturingHandler()
    logger.addHandler(handler)
    original_level = logger.level
    logger.setLevel(logging.WARNING)

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.post(
                "/api/chat",
                json={"message": "hello"},
                headers={"Authorization": "Bearer bad-token"},
            )

        assert resp.status_code == 401

        # Check that a warning was logged with relevant context
        log_messages = [r.getMessage() for r in records]
        matching = [m for m in log_messages if "401" in m]
        assert len(matching) >= 1, f"Expected 401 log, got: {log_messages}"

        log_line = matching[0]
        assert "invalid-token" in log_line or "user=" in log_line
        assert "/api/chat" in log_line
    finally:
        logger.removeHandler(handler)
        logger.setLevel(original_level)


@pytest.mark.asyncio
async def test_403_logs_user_id():
    """403 quota errors should log the actual user_id from the JWT."""
    from app.db.database import SessionLocal, User
    from app.main import app

    # Zero out quota
    db = SessionLocal()
    user = db.query(User).filter(User.id == 1).first()
    user.free_quota = 0
    user.paid_quota = 0
    db.commit()
    db.close()

    records = []

    class CapturingHandler(logging.Handler):
        def emit(self, record):
            records.append(record)

    logger = logging.getLogger("app.main")
    handler = CapturingHandler()
    logger.addHandler(handler)
    original_level = logger.level
    logger.setLevel(logging.WARNING)

    try:
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

        log_messages = [r.getMessage() for r in records]
        matching = [m for m in log_messages if "403" in m]
        assert len(matching) >= 1, f"Expected 403 log, got: {log_messages}"

        log_line = matching[0]
        assert "user=1" in log_line
        assert "/api/chat" in log_line
    finally:
        logger.removeHandler(handler)
        logger.setLevel(original_level)


@pytest.mark.asyncio
async def test_400_logs_message_too_long():
    """400 errors for message length should be logged with context."""
    from app.main import app

    records = []

    class CapturingHandler(logging.Handler):
        def emit(self, record):
            records.append(record)

    logger = logging.getLogger("app.main")
    handler = CapturingHandler()
    logger.addHandler(handler)
    original_level = logger.level
    logger.setLevel(logging.WARNING)

    try:
        token = create_token(1)
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.post(
                "/api/chat",
                json={"message": "x" * 2001},
                headers={"Authorization": f"Bearer {token}"},
            )

        assert resp.status_code == 400

        log_messages = [r.getMessage() for r in records]
        matching = [m for m in log_messages if "400" in m]
        assert len(matching) >= 1, f"Expected 400 log, got: {log_messages}"

        log_line = matching[0]
        assert "user=1" in log_line
        assert "POST" in log_line
    finally:
        logger.removeHandler(handler)
        logger.setLevel(original_level)
