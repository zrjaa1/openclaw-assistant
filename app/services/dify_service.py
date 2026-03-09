import json
from collections.abc import AsyncGenerator

import httpx

from app.config import settings


async def send_message_stream(
    query: str,
    user_id: str,
    conversation_id: str = "",
) -> AsyncGenerator[dict, None]:
    """Call Dify chat-messages API with streaming enabled.

    Yields parsed SSE event dicts. Each dict has at minimum an "event" key.
    For "message" events, "answer" contains the text chunk.
    For "message_end" events, "conversation_id" and "metadata" are included.
    """
    url = f"{settings.dify_base_url}/chat-messages"
    headers = {
        "Authorization": f"Bearer {settings.dify_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "streaming",
        "user": user_id,
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id

    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", url, json=payload, headers=headers) as resp:
            resp.raise_for_status()
            buffer = ""
            async for chunk in resp.aiter_text():
                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if line.startswith("data: "):
                        data_str = line[6:]
                        try:
                            yield json.loads(data_str)
                        except json.JSONDecodeError:
                            continue


async def send_message(
    query: str,
    user_id: str,
    conversation_id: str = "",
) -> dict:
    """Call Dify chat-messages API with blocking mode. Returns full response."""
    url = f"{settings.dify_base_url}/chat-messages"
    headers = {
        "Authorization": f"Bearer {settings.dify_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "user": user_id,
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
