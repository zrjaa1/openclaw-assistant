# OpenClaw FAQ — Common Questions & Solutions

This document covers the most common questions and issues during installation and initial setup. If you hit a problem at any step, check here first.

---

## 🔧 Installation Issues

### Q: PowerShell says "cannot be loaded" or "execution policy" (Windows)
A: This is a default Windows security restriction. To fix it:
1. Right-click PowerShell → **Run as Administrator**
2. Run this command (type `Y` and press Enter when prompted):
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Close the admin window, open a regular PowerShell, and try the install again

### Q: Installation gets stuck — progress bar isn't moving
A: Usually a network issue.
1. Press `Ctrl + C` to cancel
2. Check your internet connection
3. Try running the install command again

### Q: Node.js version is wrong or not installed
A: OpenClaw requires Node.js 22 or higher.
- Check your version: `node -v`
- If it's below 22 or not installed, go to [nodejs.org](https://nodejs.org) and download the latest LTS version
- After installing, **you must close the terminal and reopen it**

### Q: `openclaw` command not found ("is not recognized")
A: The PATH environment variable isn't set up correctly.
1. Run `npm prefix -g` to see npm's global install path
2. Add that path to your system PATH:
   - **Windows:** Settings → Search "environment variables" → Edit Path → Add the path
   - **Mac/Linux:** Run `echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc`
3. Close terminal and reopen

### Q: "npm error spawn git ENOENT"
A: You need to install Git.
- Windows: Download from [git-scm.com/downloads/win](https://git-scm.com/downloads/win)
- Mac: Run `xcode-select --install` in the terminal
- Close terminal and reopen after installing

### Q: Mac shows "Install Command Line Developer Tools" popup
A: Click **"Install"** and wait for it to complete. This is normal. Then re-run the install command.

### Q: Linux `npm install -g` says permission denied (EACCES)
A: Run these commands to fix:
```bash
mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
Then try the install again.

### Q: Can I install on Windows 7 / 32-bit systems?
A: Unfortunately no. OpenClaw requires Windows 10 or higher (64-bit). You'll need to upgrade your operating system.

---

## ⚙️ Initial Setup Issues

### Q: I pasted the API key and pressed Enter, but nothing showed on screen
A: This is normal security behavior. The command line doesn't display any characters when entering sensitive data (not even asterisks). If you pasted something, just press Enter — it was accepted.

### Q: Where do I get an API key? Does it cost money?
A: Register an account with your chosen AI provider to get a key. Popular options:
- **OpenAI:** [platform.openai.com](https://platform.openai.com) — free credits for new accounts
- **Google Gemini:** [aistudio.google.com](https://aistudio.google.com) — generous free tier
- **Anthropic:** [console.anthropic.com](https://console.anthropic.com) — limited free credits
- **DeepSeek:** [platform.deepseek.com](https://platform.deepseek.com) — free credits available

Most providers offer free tiers. Ongoing costs are typically very low ($1-$5 can last a long time).

### Q: `openclaw doctor` says network connection failed
A: Check that your API key is correct and your account has available credits. Also verify your internet connection.

### Q: I picked the wrong model — can I fix it?
A: Yes. Re-run `openclaw onboard` to change it. Your other settings won't be affected.

### Q: Where's the config file?
A: `~/.openclaw/openclaw.json`
- **Mac/Linux:** Run `open ~/.openclaw` (Mac) or `xdg-open ~/.openclaw` (Linux)
- **Windows:** In File Explorer's address bar, type `%USERPROFILE%\.openclaw`

### Q: I edited the config file — how do I apply the changes?
A: Run `openclaw gateway restart` to restart the gateway.

### Q: I broke the JSON config file format
A: OpenClaw will show an error on startup telling you what's wrong. Common mistakes:
- Missing or extra commas
- Mismatched quotes
- Mismatched brackets

You can use an online tool like [jsonlint.com](https://jsonlint.com) to check the format.

---

## 🌐 Gateway & Connection Issues

### Q: Gateway won't start
A:
1. Run `openclaw logs --follow` to see the specific error
2. Common causes: port conflict, config file format error, invalid API key
3. Try `openclaw gateway restart`

### Q: Gateway is running but the bot doesn't reply to messages
A: Check in order:
1. Is your chat platform app (Telegram bot, Discord bot, etc.) properly set up and published?
2. Are event subscriptions / webhooks correctly configured?
3. Are credentials (bot token, API key) correct?
4. Run `openclaw logs --follow` to see if messages are being received

### Q: How do I make OpenClaw start automatically when my computer boots?
A: Run `openclaw gateway install` to install it as a system service.
- Check status: `openclaw gateway status`
- Stop: `openclaw gateway stop`
- Start: `openclaw gateway start`

### Q: Pairing code expired
A: Send a new message to the bot on your chat platform. You'll get a new pairing code. Immediately run `openclaw pairing approve <platform> <new-code>` in your terminal.

---

## 💡 Usage Questions

### Q: AI responses are very slow
A:
- Check your internet connection
- Some models (especially larger ones) are naturally slower — try switching to a faster model
- Run `openclaw doctor` to check connection status

### Q: What happens when I run out of API credits?
A: The AI stops responding. Add credits on your model provider's platform to resume.

### Q: How do I check which model I'm using?
A: Send the `/model` command in the chat to see and switch models.

### Q: How do I clear chat history and start fresh?
A: Send the `/reset` command to clear the current session.

---

## 🔄 Update Questions

### Q: How do I update OpenClaw to the latest version?
A: Depending on how you installed:
- Official script: Re-run the install script (it auto-updates)
- npm: `npm update -g openclaw`

After updating, run `openclaw doctor` to confirm everything works.

### Q: Will updating erase my settings?
A: No. Config files are saved in `~/.openclaw/` — updates only replace the program itself.

---

## 🆘 Still Need Help?

**If none of the above solved your problem:**

1. Run these commands and copy the output:
   ```bash
   openclaw --version
   node -v
   openclaw doctor
   ```
2. Describe what problem you're experiencing and what you've tried
3. If there's an error message, copy it in full

You can also join the [OpenClaw Discord community](https://discord.com/invite/clawd) to ask questions, or check the official docs at [docs.openclaw.ai](https://docs.openclaw.ai).
