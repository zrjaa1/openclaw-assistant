# OpenClaw Assistant — Environment Configuration

---

## Three Environments

### 1. Local Dev
- **Purpose:** Local development and testing
- **Config method:** `.env` file (gitignored)
- **Database:** SQLite (default, no external DB needed)
- **Backend:** `http://localhost:8000`
- **Branch:** Any (local work)

### 2. Experiment (Staging)
- **Purpose:** Testing before production, preview deployments
- **Frontend:** Cloudflare Pages (preview branch)
- **Backend:** Tencent Cloud Run (experiment instance)
- **Branch:** `experiment`
- **Flow:** Test here before pushing to prod

### 3. Production
- **Purpose:** Live product for real users
- **Frontend:** Cloudflare Pages (production)
- **Backend:** Tencent Cloud Run (production instance)
- **Branch:** `main`

---

## Endpoints

### Frontend (Cloudflare Pages)

| Environment | URL | Branch |
|-------------|-----|--------|
| **Production** | https://openclaw-assistant-eg3.pages.dev | `main` |
| **Experiment** | https://experiment.openclaw-assistant-eg3.pages.dev | `experiment` |

### Backend (Tencent Cloud Run)

| Environment | URL |
|-------------|-----|
| **Production** | https://openclaw-assistant-231524-7-1409765446.sh.run.tcloudbase.com |
| **Experiment** | https://openclaw-experiment-231524-7-1409765446.sh.run.tcloudbase.com |

---

## Key Rules

1. **`.env` is local-only.** Never commit it to git.
2. **Cloudflare env vars for frontend.** `BACKEND_API_URL` is set per-environment in Cloudflare Pages → Settings → Variables and Secrets (use "Specify per environment").
3. **Test in experiment first.** Code flow: local → experiment → production.
4. **`web/config.js` is generated at deploy time.** It's gitignored — the Cloudflare build command creates it from the `BACKEND_API_URL` env var.

---

## Cloudflare Pages Configuration

- **Framework preset:** None
- **Build command:** `echo "window.BACKEND_API_URL = '${BACKEND_API_URL}';" > web/config.js`
- **Build output directory:** `web`
- **Build watch paths:** `web/*`
- **Environment variables:** `BACKEND_API_URL` — set differently per environment (Production vs Preview)

---

## Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your Dify API Key, JWT secret, etc.

# 3. Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 4. Open http://localhost:8000/web/
```

**Without a Dify API Key:** Registration, login, UI, and quota all work. Only sending messages will return a Dify connection error.

---

## AI Backend (Dify Cloud)

- **Platform:** [Dify Cloud](https://cloud.dify.ai)
- **App type:** Chat Assistant
- **Knowledge base:** Docs from `docs/` directory (bilingual zh/en)
- **LLM:** Claude Haiku 4.5 or Qwen (configurable in Dify)
- **API Key:** Set in `.env` (local) or Tencent Cloud Run env vars (remote)
