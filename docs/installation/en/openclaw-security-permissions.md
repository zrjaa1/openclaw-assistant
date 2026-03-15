# OpenClaw Security Permissions Guide

After installation and initial setup, it's a good idea to understand OpenClaw's permission levels and choose the one that fits your needs.

> 💡 Good news: Since version 2026.3.2, new installations default to "Safe Mode" — the assistant can only send and receive messages, and cannot access files or run commands. If you just installed, you're already in the safest state.
>
> ⚠️ If you installed before 2026.3.2, or manually modified the config, your OpenClaw may still be in "Full Mode." We recommend reviewing and adjusting using this guide.

---

## 4 Permission Levels

From safest to most open:

---

### 1. Safe Mode — Default, Recommended for Beginners

This is the default mode for new installations (2026.3.2+). OpenClaw can only send and receive messages.

What it CAN do:
- Send and receive messages through your chat platforms (Telegram, Discord, WhatsApp, Slack, etc.)
- View conversation history
- Check its own status

What it CANNOT do:
- Read files on your computer
- Browse the internet or search for information
- Analyze images or PDFs
- Create, modify, or delete files
- Execute terminal commands
- Save long-term memory

Best for: New users just getting started, or anyone who only needs a simple chat assistant.

If you just installed, this is already your default — no action needed.

---

### 2. Read-Only Mode

Building on Safe Mode, OpenClaw can "see" more things but still can't "touch" anything.

Additional capabilities:
- Read files on your computer (read-only, can't modify)
- Browse the internet and search for information (search must be configured separately)
- Analyze images and PDFs you send it
- Recall previously saved memories (read memory files)
- Manage conversations and sub-tasks

Still CANNOT:
- Create, modify, or delete any files
- Execute terminal commands
- Save new memories (can't write files)

Note: In Read-Only mode, OpenClaw cannot save new memories. Each new conversation starts fresh (but existing memory files can still be read). If long-term memory is important to you, consider Read & Write Mode.

Best for: Users who want the AI to help with research, read files, and analyze content — but don't want it changing anything.

To set up, copy and paste the appropriate command for your platform:

**macOS / Linux (bash/zsh):**
```bash
openclaw config set tools.deny '["write","edit","apply_patch","exec","process","sessions_spawn","nodes","canvas","cron","gateway"]'
```

**Windows (PowerShell):**
```powershell
openclaw config set tools.deny '[\"write\",\"edit\",\"apply_patch\",\"exec\",\"process\",\"sessions_spawn\",\"nodes\",\"canvas\",\"cron\",\"gateway\"]'
```

Then restart:

```
openclaw gateway restart
```

---

### 3. Read & Write Mode — Recommended for Intermediate Users

Building on Read-Only, OpenClaw can also create and modify files.

Additional capabilities:
- Create new files (e.g., write reports, organize notes)
- Modify file contents
- Save long-term memory (remembers important things you tell it across conversations)
- Write code in its workspace directory

Still CANNOT:
- Execute terminal commands (can't run programs or scripts)
- Control browsers
- Manage scheduled tasks or devices

Best for: Users who want OpenClaw to remember things, help organize files, or write code.

To set up:

**macOS / Linux (bash/zsh):**
```bash
openclaw config set tools.deny '["exec","process","sessions_spawn","nodes","canvas","cron","gateway"]'
```

**Windows (PowerShell):**
```powershell
openclaw config set tools.deny '[\"exec\",\"process\",\"sessions_spawn\",\"nodes\",\"canvas\",\"cron\",\"gateway\"]'
```

Then restart:

```
openclaw gateway restart
```

---

### 4. Full Mode — Use With Caution

OpenClaw can use all features with no restrictions. This was the default before version 2026.3.2.

Additional capabilities:
- Execute any terminal command (run programs, install software, run scripts, etc.)
- Control browsers (auto-open web pages, fill forms, click buttons, etc.)
- Manage scheduled tasks (set reminders, automation tasks, etc.)
- Control connected devices (paired phones or other computers, if any)
- Spawn sub-tasks for other AI agents

⚠️ Warning: "Full Mode" means OpenClaw can execute any operation on your computer, including running programs, installing or deleting software, etc. Unless you fully understand these permissions, this mode is not recommended.

Best for: Advanced users and developers who fully trust OpenClaw and understand all its capabilities.

To set up (same for all platforms):

```
openclaw config set tools.deny '[]'
```

Then restart:

```
openclaw gateway restart
```

---

## Quick Comparison

Safe Mode — Messages only (default, recommended for beginners)
Read-Only — Also reads files, searches web, analyzes content (can't save memories)
Read & Write — Also writes files, saves memories (recommended for intermediate users)
Full Mode — No restrictions whatsoever (use with caution)

---

## FAQ

Q: I just installed — do I need to do anything?
A: New installations (2026.3.2+) default to Safe Mode. No action needed. When you want more features, upgrade to Read-Only or Read & Write mode using the commands above.

Q: Can I change the permission level later?
A: Yes, anytime. Just re-run the appropriate command above. Remember to run `openclaw gateway restart` afterward.

Q: I chose Read-Only but now I want it to remember things?
A: Switch to Read & Write mode using the command above.

Q: How do I check my current permission level?
A: Run `openclaw status` to see your current configuration.

Q: Does web search need separate setup?
A: Yes, web search requires configuring a search API key (like Brave Search). Without it, OpenClaw works fine — it just can't proactively search the web. It can still visit specific URLs you give it.

---

Have questions? Tell me where you're stuck and I'll help.
