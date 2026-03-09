from fastapi import APIRouter, Header
from pydantic import BaseModel

from app.api.auth import verify_token
from app.db.database import SessionLocal
from app.services import quota_service

router = APIRouter()


class QuotaResponse(BaseModel):
    remaining: int


@router.get("/api/quota", response_model=QuotaResponse)
async def get_quota(authorization: str = Header(...)):
    token = authorization.removeprefix("Bearer ").strip()
    user_id = verify_token(token)

    db = SessionLocal()
    try:
        remaining = quota_service.get_remaining(db, user_id)
        return QuotaResponse(remaining=remaining)
    finally:
        db.close()
