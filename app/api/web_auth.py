import bcrypt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.api.auth import create_token
from app.config import settings
from app.db.database import SessionLocal, User

router = APIRouter()


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=6)


class AuthResponse(BaseModel):
    token: str
    remaining_quota: int


@router.post("/api/web/register", response_model=AuthResponse)
async def web_register(req: RegisterRequest):
    password_hash = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()).decode()

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == req.username).first()
        if existing:
            raise HTTPException(status_code=409, detail="用户名已被注册")

        user = User(
            openid=f"web:{req.username}",
            username=req.username,
            password_hash=password_hash,
            free_quota=settings.default_free_quota,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_token(user.id)
        remaining = user.free_quota + user.paid_quota
        return AuthResponse(token=token, remaining_quota=remaining)
    finally:
        db.close()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/api/web/login", response_model=AuthResponse)
async def web_login(req: LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == req.username).first()
        if not user or not user.password_hash:
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        if not bcrypt.checkpw(req.password.encode(), user.password_hash.encode()):
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        token = create_token(user.id)
        remaining = user.free_quota + user.paid_quota
        return AuthResponse(token=token, remaining_quota=remaining)
    finally:
        db.close()
