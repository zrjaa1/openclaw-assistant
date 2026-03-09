import httpx

from app.config import settings

WECHAT_CODE2SESSION_URL = "https://api.weixin.qq.com/sns/jscode2session"


async def code_to_session(code: str) -> dict:
    """Exchange WeChat login code for openid and session_key.

    Returns dict with keys: openid, session_key, unionid (optional), errcode, errmsg.
    """
    params = {
        "appid": settings.wechat_appid,
        "secret": settings.wechat_secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(WECHAT_CODE2SESSION_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    if "errcode" in data and data["errcode"] != 0:
        raise ValueError(f"WeChat login failed: {data.get('errmsg', 'unknown error')}")

    return data
