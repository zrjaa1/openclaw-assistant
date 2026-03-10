from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import auth, chat, quota, web_auth
from app.db.database import init_db


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


@app.get("/api/health")
async def health():
    return {"status": "ok"}


app.mount("/web", StaticFiles(directory="web", html=True), name="web")
