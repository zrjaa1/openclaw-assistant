# OpenClaw Assistant

An AI-powered installation guide for [OpenClaw](https://github.com/nicepkg/openclaw) — helping non-tech users set up and configure OpenClaw on Windows, Mac, and Linux.

OpenClaw is an open-source tool that brings AI into everyday chat apps (WeChat, Feishu, DingTalk). This assistant walks users through the installation step-by-step, with one-click copy for terminal commands.

## ⭐ Key Documentation

**Start here for project work:**

- **docs/ENVIRONMENTS.md** - Environment setup (local, experiment, production) + endpoints
- **TEST_ACCOUNTS.md** - Test account credentials for development
- **docs/basic/** and **docs/installation/** - User-facing docs (bilingual zh/en)
- **docs/system-prompt-v2.md** (English) / **docs/系统提示词-v2.md** (Chinese) - Dify system prompts

---

## Architecture

```
Cloudflare Pages (web frontend)  ┐
                                  ├→  FastAPI backend (Tencent Cloud Run)  →  Dify Cloud (RAG + LLM)
WeChat Mini Program              ┘
```

- **Backend**: Python FastAPI — authentication, conversation relay, quota management
- **Web frontend**: Single HTML file with Tailwind CSS CDN, hosted on Cloudflare Pages
- **Mini Program**: WeChat native client (same backend API)
- **AI**: Dify Cloud for RAG knowledge base + LLM (Claude Haiku / Qwen)
- **Auth**: WeChat users via `openid`; web users via username/password (bcrypt + JWT)

## Project Structure

```
app/
├── api/
│   ├── auth.py          # WeChat login + JWT token
│   ├── web_auth.py      # Web register/login (username + password + bcrypt)
│   ├── chat.py          # Chat endpoint (SSE streaming)
│   └── quota.py         # Quota query
├── db/
│   └── database.py      # SQLAlchemy models (User, Conversation, Message)
├── services/
│   ├── dify_service.py  # Dify API client
│   ├── quota_service.py # Quota deduction logic
│   └── wechat_service.py
├── config.py            # Environment config (pydantic-settings)
└── main.py              # FastAPI entry point
web/
├── index.html           # Web frontend (single file, Tailwind CSS CDN)
└── config.js            # Generated at deploy time (gitignored)
miniprogram/             # WeChat Mini Program
tests/                   # pytest tests (58 tests)
```

## Quick Start

### Backend (local development)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your Dify API Key, WeChat AppID, etc.

# 3. Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Local Testing (no cloud dependencies)

The backend is a standard FastAPI app that runs fully locally:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Minimal .env (SQLite default, no MySQL needed)
cat > .env << 'EOF'
JWT_SECRET=dev-secret-change-in-prod
DIFY_API_KEY=app-your-dify-key-here
DATABASE_URL=sqlite:///openclaw_assistant.db
DEFAULT_FREE_QUOTA=20
EOF

# 3. Start
uvicorn app.main:app --reload --port 8000

# 4. Open http://localhost:8000/web/
#    Register → Login → Send a message (requires a valid Dify API Key for replies)
```

**Without a Dify API Key**: Registration, login, UI, and quota all work. Only sending messages will return a Dify connection error.

### Running Tests

```bash
pip install -r requirements.txt -r requirements-test.txt
python3 -m pytest tests/ -v
```

All 58 tests run without external services (Dify/WeChat APIs are mocked).

### WeChat Mini Program

1. Open WeChat Developer Tools
2. Import the `miniprogram/` directory
3. Update `app.js` — set `baseUrl` to your backend URL
4. Update `project.config.json` — set `appid` to your Mini Program AppID

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/login` | WeChat login |
| POST | `/api/web/register` | Web user registration (username + password) |
| POST | `/api/web/login` | Web user login |
| POST | `/api/chat` | Send message (SSE streaming response) |
| GET | `/api/conversation/latest` | Get latest conversation history |
| GET | `/api/quota` | Query remaining message quota |
| GET | `/api/health` | Health check |
| GET | `/web/` | Web frontend (static files) |

## Deployment

### Backend — Tencent Cloud Run

The backend is deployed on Tencent Cloud Run (微信云托管). Configure via the Tencent Cloud console with production environment variables (MySQL, Dify API Key, WeChat credentials).

### Frontend — Cloudflare Pages

The `web/` directory is deployed as a static site on Cloudflare Pages.

| Environment | URL | Branch | Backend |
|-------------|-----|--------|---------|
| Production | https://openclaw-assistant-eg3.pages.dev | `main` | Tencent Cloud Run (prod) |
| Experiment | https://experiment.openclaw-assistant-eg3.pages.dev | `experiment` | Tencent Cloud Run (experiment) |

#### Setup

1. Create a **Pages** project in Cloudflare (not Workers) and connect your GitHub repo
2. Configure build settings:
   - **Framework preset**: None
   - **Build command**: `echo "window.BACKEND_API_URL = '${BACKEND_API_URL}';" > web/config.js`
   - **Build output directory**: `web`
   - **Build watch paths**: `web/*`
3. Add the `BACKEND_API_URL` environment variable under **Settings → Variables and Secrets**, using "Specify per environment" to set different backend URLs for Production and Preview
4. Deploy — pushes to `main` deploy to production, other branches get preview URLs

#### Notes

- `web/config.js` is gitignored — it's generated at deploy time by the build command from the `BACKEND_API_URL` env var
- No build tooling required (plain HTML + Tailwind CSS CDN)
- The frontend auto-detects the user's browser language (English/Chinese) and includes a manual toggle

## Configuring Dify

1. Sign up at [Dify Cloud](https://cloud.dify.ai)
2. Create an app → choose "Chat Assistant"
3. Upload knowledge base documents from the `docs/` directory
4. Configure System Prompt and LLM model (recommended: Claude Haiku 4.5 or Qwen)
5. Copy the API Key into your `.env`

## Future Considerations

- **Message ID strategy**: The `messages` table currently uses auto-increment IDs. This is optimal for single-instance MySQL (sequential B-tree inserts, no page splits). If migrating to a distributed database (Cloud Spanner, TiDB, CockroachDB), switch to ULIDs or similar (time-ordered + random suffix) to avoid write hotspotting.
- **Schema migrations**: Currently using `create_all()` which doesn't ALTER existing tables. Consider adding Alembic for production migration management.

## License

MIT
