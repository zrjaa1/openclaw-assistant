"""Test that the /api/chat endpoint returns proper SSE events,
including a 'done' event, and that a second message in the same
conversation also works correctly."""

import asyncio
import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.auth import create_token


# ---------------------------------------------------------------------------
# Fake Dify stream generator
# ---------------------------------------------------------------------------

async def fake_dify_stream(query, user_id, conversation_id=""):
    """Simulate Dify SSE events: several message chunks + message_end."""
    chunks = ["Hello", ", this is ", "a test reply."]
    for chunk in chunks:
        yield {"event": "message", "answer": chunk}
        await asyncio.sleep(0)  # let the event loop tick
    yield {
        "event": "message_end",
        "conversation_id": "dify-conv-abc123",
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_sse_events(body: str) -> list[dict]:
    """Parse SSE text into a list of data dicts."""
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
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_first_message_returns_done_event(mock_dify):
    """First chat message should return message chunks + a done event."""
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/chat",
            json={"message": "hello"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    events = parse_sse_events(resp.text)

    # Should have message events + exactly one done event
    msg_events = [e for e in events if e.get("type") == "message"]
    done_events = [e for e in events if e.get("type") == "done"]

    assert len(msg_events) >= 1, f"Expected message events, got: {events}"
    assert len(done_events) == 1, f"Expected exactly 1 done event, got: {events}"

    # done event should include a conversation_id
    assert done_events[0]["conversation_id"] is not None

    # Concatenated content should match
    full_text = "".join(e["content"] for e in msg_events)
    assert full_text == "Hello, this is a test reply."


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_second_message_works(mock_dify):
    """After a first message, sending a second message in the same
    conversation should succeed and also return a done event."""
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # First message
        resp1 = await client.post(
            "/api/chat",
            json={"message": "hello"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp1.status_code == 200
        events1 = parse_sse_events(resp1.text)
        done1 = [e for e in events1 if e.get("type") == "done"][0]
        conv_id = done1["conversation_id"]

        # Second message using the conversation_id from the first
        resp2 = await client.post(
            "/api/chat",
            json={"message": "next question", "conversation_id": conv_id},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp2.status_code == 200
    events2 = parse_sse_events(resp2.text)

    msg_events2 = [e for e in events2 if e.get("type") == "message"]
    done_events2 = [e for e in events2 if e.get("type") == "done"]

    assert len(msg_events2) >= 1, f"Second message had no message events: {events2}"
    assert len(done_events2) == 1, f"Second message missing done event: {events2}"

    # Verify mock was called with the Dify conversation_id for continuity
    second_call = mock_dify.call_args_list[1]
    assert second_call.kwargs.get("conversation_id") == "dify-conv-abc123" or \
           second_call[1].get("conversation_id") == "dify-conv-abc123", \
        f"Second call should pass Dify conversation_id, got: {second_call}"


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_latest_conversation_restored(mock_dify):
    """After sending a message, GET /api/conversation/latest should return it."""
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Send a message first
        await client.post(
            "/api/chat",
            json={"message": "hello"},
            headers={"Authorization": f"Bearer {token}"},
        )

        # Now fetch latest conversation
        resp = await client.get(
            "/api/conversation/latest",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["conversation_id"] is not None
    assert len(data["messages"]) == 2  # user + assistant
    assert data["messages"][0]["role"] == "user"
    assert data["messages"][0]["content"] == "hello"
    assert data["messages"][1]["role"] == "assistant"


@pytest.mark.asyncio
async def test_latest_conversation_empty():
    """When no conversation exists, return null conversation_id."""
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get(
            "/api/conversation/latest",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    assert resp.json()["conversation_id"] is None
    assert resp.json()["messages"] == []


@pytest.mark.asyncio
@patch("app.api.chat.dify_service.send_message_stream", side_effect=fake_dify_stream)
async def test_sse_format_has_proper_newlines(mock_dify):
    """Each SSE data line should be followed by double newlines,
    so the frontend can split and parse them correctly."""
    from app.main import app

    token = create_token(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/chat",
            json={"message": "hello"},
            headers={"Authorization": f"Bearer {token}"},
        )

    body = resp.text
    # Each "data: " line should be followed by "\n\n"
    import re
    data_lines = re.findall(r"data: .+", body)
    assert len(data_lines) >= 2, f"Expected multiple data lines, got: {data_lines}"

    # Verify double newline separators exist
    assert "\n\n" in body, "SSE events should be separated by double newlines"
