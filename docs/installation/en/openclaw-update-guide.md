# OpenClaw Update & Upgrade Guide

OpenClaw continuously releases new versions with bug fixes and features. This guide shows you how to safely update to the latest version.

> 💡 **Tip:** Updating only replaces the program itself. Your config files, API keys, and chat history won't be lost.

---

## 🚀 How to Update

Choose the update method that matches how you originally installed:

### Method 1: Re-run the Install Script (Simplest, Recommended)

No matter how you originally installed, re-running the install script will update you:

**Mac / Linux:**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

**Windows (PowerShell):**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

> 💡 **Tip:** The `--no-onboard` flag skips the setup wizard (your config is already set up, no need to redo it).

### Method 2: Using npm

```bash
npm update -g openclaw
```

---

## ✅ Verify After Updating

After the update, run these commands to confirm everything works:

```bash
openclaw --version
openclaw doctor
openclaw gateway restart
```

1. `--version` — Confirm the version number has updated
2. `doctor` — Full health check, detects if config needs migration
3. `gateway restart` — Restart the gateway so the new version takes effect

> 💡 **Tip:** `openclaw doctor` automatically fixes some config changes from version upgrades, so always run it after updating.

---

## ❓ FAQ

**Q: Will updating erase my settings?**
A: No. Your config is saved in `~/.openclaw/` — updates only replace the program itself.

**Q: The bot stopped working after updating — what do I do?**
A:
1. Run `openclaw doctor` first — it detects and fixes most issues
2. Run `openclaw gateway restart` to restart the gateway
3. If it's still broken, check the logs: `openclaw logs --follow`

**Q: How do I roll back to an older version?**
A: Install a specific version (replace `1.2.3` with the version you want):
```bash
npm install -g openclaw@1.2.3
openclaw doctor
openclaw gateway restart
```

**Q: How do I know if there's a new version?**
A: OpenClaw automatically checks for updates on startup and shows a notice in the logs. You can also run the install script or `npm update` anytime to get the latest.

---

*Update issues? Share the output of `openclaw doctor` and I'll help troubleshoot.*
