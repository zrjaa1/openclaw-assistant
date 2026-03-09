from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.db.database import SessionLocal, User

router = APIRouter()


class LoginRequest(BaseModel):
    code: str


class LoginResponse(BaseModel):
    token: str
    remaining_quota: int


def create_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=30),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def verify_token(token: str) -> int:
    """Verify JWT token and return user_id. Raises HTTPException on failure."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/api/debug/users")
async def debug_users():
    """Temporary debug endpoint to list all users. Remove before production."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return [
            {
                "id": u.id,
                "openid": u.openid,
                "free_quota": u.free_quota,
                "paid_quota": u.paid_quota,
            }
            for u in users
        ]
    finally:
        db.close()


@router.post("/api/login", response_model=LoginResponse)
async def login(req: LoginRequest):
    from app.services.wechat_service import code_to_session

    try:
        wx_data = await code_to_session(req.code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"WeChat API error: {e}")

    openid = wx_data.get("openid")
    if not openid:
        raise HTTPException(status_code=502, detail=f"WeChat returned no openid: {wx_data}")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.openid == openid).first()
        if not user:
            user = User(
                openid=openid,
                free_quota=settings.default_free_quota,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        token = create_token(user.id)
        remaining = user.free_quota + user.paid_quota
        return LoginResponse(token=token, remaining_quota=remaining)
    finally:
        db.close()
