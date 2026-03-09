"""Tests for the Dify service (streaming and blocking)."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.dify_service import send_message, send_message_stream


class FakeStreamResponse:
    """Simulates httpx streaming response with SSE data."""

    def __init__(self, lines):
        self._lines = lines

    def raise_for_status(self):
        pass

    async def aiter_text(self):
        for line in self._lines:
            yield line + "\n"


class FakeStreamContextManager:
    def __init__(self, lines):
        self._resp = FakeStreamResponse(lines)

    async def __aenter__(self):
        return self._resp

    async def __aexit__(self, *args):
        pass


class FakeAsyncClient:
    """Mock httpx.AsyncClient that supports both async-with and .stream()."""

    def __init__(self, stream_cm):
        self._stream_cm = stream_cm
        self.stream_calls = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    def stream(self, *args, **kwargs):
        self.stream_calls.append((args, kwargs))
        return self._stream_cm


def _make_fake_client(sse_lines):
    cm = FakeStreamContextManager(sse_lines)
    return FakeAsyncClient(cm)


@pytest.mark.asyncio
async def test_send_message_stream_yields_events():
    sse_lines = [
        'data: {"event": "message", "answer": "Hello"}',
        'data: {"event": "message", "answer": " world"}',
        'data: {"event": "message_end", "conversation_id": "conv-1"}',
    ]
    fake_client = _make_fake_client(sse_lines)

    with patch("app.services.dify_service.httpx.AsyncClient", return_value=fake_client):
        events = []
        async for event in send_message_stream("test", "user1"):
            events.append(event)

    assert len(events) == 3
    assert events[0]["event"] == "message"
    assert events[0]["answer"] == "Hello"
    assert events[1]["answer"] == " world"
    assert events[2]["event"] == "message_end"
    assert events[2]["conversation_id"] == "conv-1"


@pytest.mark.asyncio
async def test_send_message_stream_skips_invalid_json():
    sse_lines = [
        'data: {"event": "message", "answer": "ok"}',
        "data: NOT VALID JSON",
        'data: {"event": "message_end", "conversation_id": "c1"}',
    ]
    fake_client = _make_fake_client(sse_lines)

    with patch("app.services.dify_service.httpx.AsyncClient", return_value=fake_client):
        events = []
        async for event in send_message_stream("test", "user1"):
            events.append(event)

    assert len(events) == 2


@pytest.mark.asyncio
async def test_send_message_stream_passes_conversation_id():
    sse_lines = ['data: {"event": "message_end", "conversation_id": "c1"}']
    fake_client = _make_fake_client(sse_lines)

    with patch("app.services.dify_service.httpx.AsyncClient", return_value=fake_client):
        async for _ in send_message_stream("q", "u1", conversation_id="existing-conv"):
            pass

    # Verify the payload included conversation_id
    call_args, call_kwargs = fake_client.stream_calls[0]
    payload = call_kwargs.get("json")
    assert payload["conversation_id"] == "existing-conv"


@pytest.mark.asyncio
async def test_send_message_blocking():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "answer": "Full reply",
        "conversation_id": "conv-1",
    }
    mock_resp.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.post.return_value = mock_resp

    with patch("app.services.dify_service.httpx.AsyncClient") as mock_cls:
        mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await send_message("test query", "user1")

    assert result["answer"] == "Full reply"
    assert result["conversation_id"] == "conv-1"
