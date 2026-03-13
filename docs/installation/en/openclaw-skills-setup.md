# OpenClaw Skills Getting Started Guide

OpenClaw "skills" are like apps for your AI assistant — they teach it new abilities. For example: checking the weather, controlling smart lights, managing notes, and more. This guide covers the basics and walks you through installing your first skill.

> 💡 **Tip:** Skills are optional enhancements. OpenClaw works perfectly fine for chatting without any skills installed. Add skills when you want your AI assistant to do more.

---

## ✅ Prerequisites

- ✅ **OpenClaw is installed and configured** — `openclaw doctor` shows all green
- ✅ **Gateway is running** — `openclaw gateway status` shows `running`

> ⚠️ **Haven't finished basic setup?** Complete initial configuration first (choose an AI model, enter your API key), confirm `openclaw doctor` is all green, then come back here.

---

## 🤔 What Are Skills?

In simple terms:

| Concept | Analogy | Description |
| :--- | :--- | :--- |
| **OpenClaw itself** | A smartphone | The base AI chat platform |
| **Skills** | Apps on the phone | Add new capabilities to the AI assistant |
| **Plugins** | Communication modules | Connect to new chat platforms (Telegram, Discord, etc.) |

**Skills vs Plugins:**
- **Plugins** connect OpenClaw to chat platforms (Telegram, Discord, WhatsApp, Slack, etc.)
- **Skills** teach the AI assistant new abilities (check weather, control lights, search the web, etc.)

> 💡 **Tip:** OpenClaw comes with some built-in skills. You can check what's available and add more at any time.

---

## 🚀 Step 1: See What Skills You Have

Open your terminal and run:

```bash
openclaw skills list
```

This shows all available skills:
- ✅ **Active** skills (all requirements met, loaded)
- ⚠️ **Inactive** skills (missing something, like an extra tool or API key)

To see details about a specific skill:

```bash
openclaw skills info <skill-name>
```

For example, to check the weather skill:

```bash
openclaw skills info weather
```

---

### ❓ FAQ

**Q: The skill list is huge — how do I see only active ones?**
A: Run `openclaw skills list --eligible` to show only skills that are ready to use.

**Q: The skill list is empty?**
A: That shouldn't happen normally. Run `openclaw skills check` to diagnose skill loading.

---

## 📋 Step 2: Install New Skills

There are two ways to install skills:

### Method 1: From ClawHub (Recommended)

ClawHub is OpenClaw's skill marketplace where you can browse and install community-built skills.

**Browse skills:** Open [https://clawhub.com](https://clawhub.com) in your browser

**Install a skill:** In your terminal, run (replace `<skill-name>` with the one you want):

```bash
clawhub install <skill-name>
```

### Method 2: Manual Install

If you know the npm package name, you can install directly:

```bash
openclaw plugins install <package-name>
```

> 💡 **Tip:** Method 1 (ClawHub) is enough for most users — simple and intuitive.

---

### ❓ FAQ

**Q: `clawhub` command not found?**
A: ClawHub CLI may need separate installation:
```bash
npm install -g clawhub
```

**Q: Do I need to restart OpenClaw after installing a skill?**
A: No. OpenClaw automatically detects new skills and loads them in the next conversation.

---

## 🛠️ Step 3: Configure Skills

Some skills work right out of the box (like weather), while others need extra setup (like a third-party API key).

### Check If a Skill Needs Configuration

```bash
openclaw skills info <skill-name>
```

If the output mentions an API key or environment variable, add it to your config file:

```json5
// ~/.openclaw/openclaw.json
{
  "skills": {
    "entries": {
      "skill-name": {
        "enabled": true,
        "env": {
          "SOME_API_KEY": "your-key-here"
        }
      }
    }
  }
}
```

### Enable/Disable a Skill

To turn off a skill:

```json5
{
  "skills": {
    "entries": {
      "some-skill": {
        "enabled": false
      }
    }
  }
}
```

---

### ❓ FAQ

**Q: Where's the config file?**
A: `~/.openclaw/openclaw.json`
- Mac/Linux: Run `open ~/.openclaw` (Mac) or `xdg-open ~/.openclaw` (Linux)
- Windows: Type `%USERPROFILE%\.openclaw` in File Explorer's address bar

**Q: How do I apply config changes?**
A: Skill config changes take effect in the next new conversation. To apply immediately, restart the gateway:
```bash
openclaw gateway restart
```

---

## 📋 Recommended Starter Skills

These useful skills work out of the box — no extra configuration needed:

| Skill | What It Does | Install |
| :--- | :--- | :--- |
| **weather** | Weather lookups and forecasts | Built-in, no install needed |
| **web-search** | Search the web (needs search engine config) | Built-in, needs search setup |

> 💡 **Tip:** Browse [clawhub.com](https://clawhub.com) for more. The community is constantly building new skills!

---

## 📋 Quick Reference: Commands

| Command | What It Does |
| :--- | :--- |
| `openclaw skills list` | List all skills |
| `openclaw skills list --eligible` | Show only active skills |
| `openclaw skills info <name>` | View skill details |
| `openclaw skills check` | Diagnose skill loading |
| `clawhub install <name>` | Install a skill from ClawHub |
| `openclaw plugins list` | List all plugins |
| `openclaw plugins install <pkg>` | Install a plugin |

---

## ❓ General FAQ

**Q: What's the relationship between skills and plugins?**
A: They're different things:
- **Skills** = AI assistant abilities (weather, lights, search, etc.)
- **Plugins** = Chat platform connections (Telegram, Discord, etc.)
Both can be installed and used independently.

**Q: Will too many skills slow down the AI?**
A: Each skill uses a small amount of the AI's "attention" (context window), but the impact is usually negligible. If you notice slower responses, you can disable skills you don't use often.

**Q: Do skills auto-update?**
A: No. Update manually with:
```bash
clawhub update --all
```

**Q: Can I build my own skills?**
A: Yes! A skill is essentially a folder with a `SKILL.md` file. The OpenClaw docs have a detailed development guide for technically inclined users.

**Q: Is it safe to install skills?**
A: ClawHub skills are community-maintained. As with any third-party software, only install skills you trust. OpenClaw performs basic safety checks during installation.

---

*Questions? Join the [OpenClaw Discord community](https://discord.com/invite/clawd) to ask.*
