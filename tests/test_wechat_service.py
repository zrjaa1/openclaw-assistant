"""Tests for the WeChat service (code_to_session)."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.services.wechat_service import code_to_session


def _make_mock_client(response_data, status_code=200):
    """Build a mock httpx.AsyncClient with the given response."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = response_data
    mock_resp.status_code = status_code
    mock_resp.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_resp
    return mock_client


@pytest.mark.asyncio
async def test_code_to_session_success():
    mock_client = _make_mock_client({"openid": "o123", "session_key": "sk"})

    with patch("app.services.wechat_service.settings") as mock_settings:
        mock_settings.wechat_appid = "wx_test"
        mock_settings.wechat_secret = "secret_test"

        with patch("app.services.wechat_service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
            mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await code_to_session("valid-code")

    assert result["openid"] == "o123"


@pytest.mark.asyncio
async def test_code_to_session_wechat_error():
    mock_client = _make_mock_client({"errcode": 40029, "errmsg": "invalid code"})

    with patch("app.services.wechat_service.settings") as mock_settings:
        mock_settings.wechat_appid = "wx_test"
        mock_settings.wechat_secret = "secret_test"

        with patch("app.services.wechat_service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
            mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            with pytest.raises(ValueError, match="invalid code"):
                await code_to_session("bad-code")


@pytest.mark.asyncio
async def test_code_to_session_missing_config():
    with patch("app.services.wechat_service.settings") as mock_settings:
        mock_settings.wechat_appid = ""
        mock_settings.wechat_secret = ""

        with pytest.raises(ValueError, match="must be configured"):
            await code_to_session("any-code")
