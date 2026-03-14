# Test Accounts — OpenClaw Assistant

**Purpose:** Accounts for development and testing across all environments.

**Security:** These are test accounts. Do NOT use real credentials.

**Last updated:** 2026-03-13

---

## Experiment Environment

### Test Account #1
- **Username:** testuser
- **Password:** TestPass2024!
- **Backend:** https://openclaw-experiment-231524-7-1409765446.sh.run.tcloudbase.com
- **Frontend:** https://experiment.openclaw-assistant-eg3.pages.dev
- **Quota:** 20 messages (default)
- **Created:** 2026-03-13
- **Last verified:** 2026-03-13 ✅ (register + login verified via API)

---

## Production Environment

### Test Account #1
- **Username:** testuser
- **Password:** TestPass2024!
- **Backend:** https://openclaw-assistant-231524-7-1409765446.sh.run.tcloudbase.com
- **Frontend:** https://openclaw-assistant-eg3.pages.dev
- **Quota:** 100 messages
- **Created:** 2026-03-13
- **Last verified:** 2026-03-13 ✅ (register + login verified via API)

---

## Local Development

- Local dev uses SQLite — each developer gets their own isolated database
- Register via the web frontend at `http://localhost:8000/web/` or via API:
  ```
  curl -X POST http://localhost:8000/api/web/register \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser","password":"TestPass2024!"}'
  ```
- Default quota: 20 messages (configurable via `DEFAULT_FREE_QUOTA` in `.env`)
- No persistent test accounts — SQLite DB is ephemeral (gitignored)

---

## Notes

- Web accounts are created via `/api/web/register` endpoint or the web UI sign-up form
- WeChat accounts are auto-created on first login via `/api/login` (requires WeChat Developer Tools)
- Production has a higher default quota (100) than experiment (20)
- ⚠️ `BACKEND_API_URL` in `.env.example` is for Cloudflare build only — the Python backend rejects it as an unknown field. Remove it from `.env` when running locally, or add `backend_api_url` to `app/config.py` Settings class.
