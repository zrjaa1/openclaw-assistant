# Local Development — OpenClaw Assistant

## Prerequisites

- Python 3.12+ (tested on 3.14)
- No external services required for basic testing

## Quick Start

```bash
cd /Users/hendrix/.openclaw/workspace/projects/openclaw-assistant

# Activate venv
source .venv/bin/activate

# Create .env for local dev
cat > .env << 'EOF'
JWT_SECRET=dev-secret-local-testing
DIFY_API_KEY=app-placeholder-no-dify
DIFY_BASE_URL=https://api.dify.ai/v1
DATABASE_URL=sqlite:///openclaw_assistant.db
DEFAULT_FREE_QUOTA=20
EXEMPT_OPENIDS=
WECHAT_APPID=wx-placeholder
WECHAT_SECRET=placeholder
EOF

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Open web UI
open http://localhost:8000/web/
```

## What Works Without Dify

- ✅ Web registration & login
- ✅ Quota checking
- ✅ Health endpoint
- ✅ Web UI loads and renders
- ❌ Chat messages (returns Dify 401 — needs valid API key)

## Running Tests

```bash
source .venv/bin/activate
pip install pytest pytest-asyncio  # first time only
python3 -m pytest tests/ -v
```

All 58 tests pass (mocked, no external deps).

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/web/register` | None | Register (username+password) |
| POST | `/api/web/login` | None | Login → JWT token |
| POST | `/api/login` | None | WeChat login (openid) |
| POST | `/api/chat` | Bearer JWT | Send message (SSE stream) |
| GET | `/api/quota` | Bearer JWT | Check remaining quota |
| GET | `/api/conversation/latest` | Bearer JWT | Recent conversation |
| GET | `/api/health` | None | Health check |
| GET | `/web/` | None | Web frontend |

## Notes

- `.env` and `openclaw_assistant.db` are gitignored
- WeChat Mini Program is in `miniprogram/` — requires WeChat DevTools
- Dify setup: see main README.md
