# OpenClaw Initial Setup & AI Model Configuration Guide

After installing OpenClaw, the next step is to connect an AI "brain" (a large language model). This guide walks you through the minimum setup to get OpenClaw up and running.

> 💡 **Tip:** The goal here is to get things working first. We'll skip optional features (chat platform integrations, skills, etc.) and come back to them later.

---

## ✅ Before You Start: Confirm Installation

First, make sure OpenClaw is properly installed:

```bash
openclaw --version
```

If you see a version number (like `1.x.x`), you're good to go.

> ⚠️ **If it says "command not found" or "is not recognized":** Installation isn't complete or PATH isn't set up. Please go back to the installation guide to finish, or tell me what's happening and I'll help troubleshoot.

---

## 🚀 Step 1: Launch the Setup Wizard

Open your command line (PowerShell on Windows, Terminal on Mac/Linux) and type:

```bash
openclaw onboard
```

> 💡 **Tip:** If you want OpenClaw to automatically run in the background when your computer starts, use `openclaw onboard --install-daemon` instead. This is recommended.

---

## 📋 Step 2: Follow the Wizard Prompts

The wizard uses **arrow keys** to navigate and **Enter** to confirm. Here are the recommended choices for each step:

### Option 1: Safety Confirmation
> **I understand this is personal-by-default and shared/multi-user use requires lock-down. Continue?**

Choose **Yes** — This just confirms that OpenClaw defaults to personal-use mode.

### Option 2: Setup Mode
> **Onboarding mode**

Choose **QuickStart** — Fast mode that skips advanced options. Best for new users.

### Option 3: AI Model Provider (The Most Important Step)
> **Model/auth provider**

This is where you choose the "brain" for your AI assistant.

**Popular choices:**

| Provider | Strengths | Free Tier? |
| :--- | :--- | :--- |
| **OpenAI (GPT)** | Most well-known, great all-around | Yes (free credits for new accounts) |
| **Google (Gemini)** | Strong multimodal, generous free tier | Yes (very generous) |
| **Anthropic (Claude)** | Excellent reasoning and nuance | Yes (limited free credits) |
| **DeepSeek** | Outstanding value, strong reasoning | Yes |
| **OpenRouter** | Access many models with one key | Varies by model |

> 💡 **Tip:** Not sure which to pick? **Google Gemini** is a great starting point — generous free tier, easy to set up, and good performance. **OpenAI** is also a solid choice if you're already familiar with ChatGPT.

### Option 4: Enter API Key
> **API Key**

Paste your API key here. An API key is a "pass" you get from your AI model provider.

**Don't have an API key yet?** Here's where to get one:

| Provider | Sign-Up URL | Notes |
| :--- | :--- | :--- |
| **OpenAI** | [platform.openai.com](https://platform.openai.com) | Create account → API Keys → Create new key |
| **Google Gemini** | [aistudio.google.com](https://aistudio.google.com) | Sign in with Google → Get API Key |
| **Anthropic** | [console.anthropic.com](https://console.anthropic.com) | Create account → API Keys |
| **DeepSeek** | [platform.deepseek.com](https://platform.deepseek.com) | Create account → API Keys |
| **OpenRouter** | [openrouter.ai](https://openrouter.ai) | Sign in → Keys → Create Key |

> ⚠️ **Note:** When pasting the API key, the screen **won't show any characters** (not even asterisks). This is a security feature of the command line — it's not a bug. Just paste and press Enter.

### Option 5: Choose a Specific Model
> **Select Model**

Pick the **default option or the first one** in the list. You can always switch later with the `/model` command.

### Option 6: Communication Channel
> **Select channel (QuickStart)**

Choose **Skip for now** — Setting up Telegram, Discord, WhatsApp, etc. takes extra steps. We'll do it later. For now, just skip.

### Option 7: Search Engine
> **Search Provider**

Choose **Skip for now** — Search is optional. Add it later when you need it.

### Option 8: Skills
> **Configure skills now?**

Choose **No** — Skills are optional enhancements. Not needed for basic operation.

### Option 9: Background Service
> **Install Daemon**

Choose **Yes** — This keeps OpenClaw running in the background even after you close the terminal window.

---

### ❓ Setup Wizard FAQ

**Q: I pasted the API key and pressed Enter but nothing happened?**
A: The command line doesn't show any characters when entering sensitive data (not even asterisks). This is normal security behavior. If you did paste the key, it should have been accepted — continue to the next step.

**Q: I picked the wrong model — can I change it?**
A: No worries. You can re-run `openclaw onboard` at any time to change it, or edit the config file directly.

**Q: Where do I get an API key? Does it cost money?**
A: Each provider requires you to create an account first. Most providers offer **free credits** for new accounts — usually enough for personal use. When free credits run out, costs are typically very low ($1-$5 can last a long time for casual use).

**Q: The wizard exited halfway through?**
A: Just run `openclaw onboard` again. Existing config won't be affected.

---

## 🔒 Step 3: Set Security Permissions (Important!)

After the wizard finishes, we strongly recommend setting an appropriate permission level before you start using OpenClaw.

Since version 2026.3.2, new installations default to "Safe Mode" — the assistant can only send and receive messages. If you upgraded from an older version, you may still be on "Full Mode" — we recommend adjusting.

**There are 4 permission levels:**

**1. Safe Mode — Default for new installs, recommended for beginners**

Can only send and receive messages. Cannot read/write files or run commands. If you just installed (version 2026.3.2+), you're already here — no action needed.

**2. Read-Only Mode**

Adds the ability to read local files, browse the web, analyze images and PDFs, and read memory. Cannot create or modify files. Note: cannot save new memories.

Copy and paste the appropriate command for your platform:

macOS / Linux (bash/zsh):
```bash
openclaw config set tools.deny '["write","edit","apply_patch","exec","process","sessions_spawn","nodes","canvas","cron","gateway"]'
```

Windows (PowerShell):
```powershell
openclaw config set tools.deny '[\"write\",\"edit\",\"apply_patch\",\"exec\",\"process\",\"sessions_spawn\",\"nodes\",\"canvas\",\"cron\",\"gateway\"]'
```

**3. Read & Write Mode — Recommended for intermediate users**

Adds the ability to create and modify files and save long-term memory. Cannot execute terminal commands.

macOS / Linux (bash/zsh):
```bash
openclaw config set tools.deny '["exec","process","sessions_spawn","nodes","canvas","cron","gateway"]'
```

Windows (PowerShell):
```powershell
openclaw config set tools.deny '[\"exec\",\"process\",\"sessions_spawn\",\"nodes\",\"canvas\",\"cron\",\"gateway\"]'
```

**4. Full Mode — Advanced users only, use with caution**

No restrictions at all. Can execute commands, control browsers, manage devices, etc. This was the default before version 2026.3.2. ⚠️ Unless you fully understand these permissions, this is not recommended.

```
openclaw config set tools.deny '[]'
```

**After setting permissions, restart OpenClaw:**

```
openclaw gateway restart
```

> 💡 **Tip:** New installations are already in Safe Mode — you can skip this step. When you need more capabilities, run the appropriate command above to upgrade.

---

## 🛠️ Step 4: Health Check

After setup, run a full health check:

```bash
openclaw doctor
```

**What to look for:**
- All items show green `✓` → Perfect, everything is ready! 🎉
- Mostly green with a few yellow `⚠` → Basically fine — yellow usually means optional features aren't configured
- Any red `✗` → Something needs fixing — share the error message with me

---

### ❓ Health Check FAQ

**Q: `openclaw doctor` says network connection failed?**
A: Check that your API key is correct and your account has available credits. Also verify your internet connection is working.

**Q: It says the model connection timed out?**
A: Could be temporary network instability. Wait a few minutes and run `openclaw doctor` again. If it keeps timing out, consider switching to a different model provider.

---

## 🎉 Step 5: Start Using OpenClaw

Congratulations! Basic setup is complete. Here's the quickest way to get started:

### Open the Dashboard (Recommended for New Users)

```bash
openclaw dashboard
```

This opens a web interface in your browser where you can chat with your AI assistant right away.

### Or Chat Directly in the Terminal

```bash
openclaw
```

---

## 📋 Quick Reference: Common Commands

| Command | What It Does |
| :--- | :--- |
| `openclaw onboard` | Re-run the setup wizard (change model, API key, etc.) |
| `openclaw dashboard` | Open the browser-based control panel |
| `openclaw doctor` | Full health check (test config and connections) |
| `openclaw gateway start` | Start the background service |
| `openclaw gateway stop` | Stop the background service |
| `openclaw gateway status` | Check background service status |
| `openclaw status` | View current configuration |

---

## ❓ General FAQ

**Q: Setup is done — what can I do next?**
A: The basic version lets you chat with the AI via `openclaw dashboard`. If you want to connect it to Telegram, Discord, WhatsApp, or other platforms, I can guide you through it.

**Q: How do I switch to a different AI model?**
A: Re-run `openclaw onboard` and choose a new model at that step. Your other settings won't be lost.

**Q: What happens when I run out of API credits?**
A: The AI assistant will stop responding, and you'll see an error like "insufficient balance." Just add credits on your model provider's platform to resume.

**Q: Can I configure multiple AI models?**
A: Yes, but that's an advanced setup. We recommend getting one model running first, then I can help you configure multi-model switching later.

---

*Have questions? Tell me which step you're stuck on and I'll help you out.*
