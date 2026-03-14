# Test Accounts — OpenClaw Assistant

**Purpose:** Accounts for development and testing of the web frontend.

**Security:** These are test accounts with no real data. Do NOT use real credentials.

**Last updated:** 2026-03-13

---

## Web Frontend Test Account

### Test Account #1 (General Testing)
- **Username:** testuser
- **Password:** TestPass2024!
- **Environment:** Local dev (`http://localhost:8000/web/`)
- **Created:** _TBD (create on first local dev session)_
- **Purpose:** General UI testing, chat flow, quota verification
- **Notes:** Register via the web frontend's sign-up form. SQLite DB is local-only.

---

## WeChat Mini Program Test Account

- **OpenID:** _Requires WeChat Developer Tools_
- **Environment:** Local dev with WeChat mock
- **Notes:** WeChat testing requires a valid AppID and Developer Tools setup. See `miniprogram/` README for details.

---

## Notes

- Local dev uses SQLite by default — each developer gets their own isolated database
- Web accounts are created via the `/api/web/register` endpoint or the web UI
- WeChat accounts are auto-created on first login via `/api/login`
- Quota defaults to 20 free messages per user (configurable via `DEFAULT_FREE_QUOTA` in `.env`)
