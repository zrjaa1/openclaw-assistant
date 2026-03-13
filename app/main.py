import logging
from contextlib import asynccontextmanager

import jwt
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api import auth, chat, quota, web_auth
from app.config import settings
from app.db.database import init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.config import settings

    db_type = settings.database_url.split("://")[0] if "://" in settings.database_url else "unknown"
    print(f"[startup] database backend: {db_type}")
    init_db()
    yield


app = FastAPI(
    title="OpenClaw Assistant",
    description="OpenClaw 安装与使用助手 API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["auth"])
app.include_router(chat.router, tags=["chat"])
app.include_router(quota.router, tags=["quota"])
app.include_router(web_auth.router, tags=["web-auth"])


def _extract_user_id(request: Request) -> str:
    """Best-effort extraction of user_id from the Authorization header."""
    auth_header = request.headers.get("authorization", "")
    token = auth_header.removeprefix("Bearer ").strip()
    if not token:
        return "anonymous"
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"],
                             options={"verify_exp": False})
        return str(payload.get("user_id", "unknown"))
    except Exception:
        return "invalid-token"


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Log all HTTP errors (4xx/5xx) with user and request context."""
    user_id = _extract_user_id(request)
    logger.warning(
        "%s %s -> %d %s | user=%s ip=%s",
        request.method,
        request.url.path,
        exc.status_code,
        exc.detail,
        user_id,
        request.client.host if request.client else "unknown",
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/api/health")
async def health():
    return {"status": "ok"}


app.mount("/web", StaticFiles(directory="web", html=True), name="web")
