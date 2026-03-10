"""Tests for quota exemption logic."""

from unittest.mock import patch

import pytest

from app.db.database import SessionLocal, User
from app.services.quota_service import check_and_deduct, get_remaining


@patch("app.services.quota_service.settings")
def test_exempt_user_has_unlimited_quota(mock_settings):
    """An exempt user should see 999999 remaining quota."""
    mock_settings.exempt_openids = "test-openid"

    db = SessionLocal()
    remaining = get_remaining(db, user_id=1)
    db.close()

    assert remaining == 999999


@patch("app.services.quota_service.settings")
def test_exempt_user_not_deducted(mock_settings):
    """An exempt user should not have quota deducted."""
    mock_settings.exempt_openids = "test-openid"

    db = SessionLocal()
    assert check_and_deduct(db, user_id=1) is True
    user = db.query(User).filter(User.id == 1).first()
    assert user.free_quota == 10  # unchanged
    db.close()


@patch("app.services.quota_service.settings")
def test_non_exempt_user_not_affected(mock_settings):
    """A user not in the exempt list should have normal quota behavior."""
    mock_settings.exempt_openids = "other-openid"

    db = SessionLocal()
    remaining = get_remaining(db, user_id=1)
    db.close()

    assert remaining == 10  # normal quota


@patch("app.services.quota_service.settings")
def test_empty_exempt_list(mock_settings):
    """When exempt list is empty, no one is exempt."""
    mock_settings.exempt_openids = ""

    db = SessionLocal()
    remaining = get_remaining(db, user_id=1)
    db.close()

    assert remaining == 10


@patch("app.services.quota_service.settings")
def test_multiple_exempt_openids(mock_settings):
    """Comma-separated exempt list should work correctly."""
    mock_settings.exempt_openids = "other-id, test-openid, another-id"

    db = SessionLocal()
    remaining = get_remaining(db, user_id=1)
    db.close()

    assert remaining == 999999
