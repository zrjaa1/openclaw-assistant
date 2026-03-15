# OpenClaw macOS & Linux Installation Guide

This guide helps Mac and Linux users install OpenClaw. Installation on Mac and Linux is usually smoother than Windows, but we'll explain every step in detail. Don't worry if you run into issues — most have straightforward fixes.

---

## ✅ Before You Start: Check Your System

| Requirement | How to Check | Minimum |
| :--- | :--- | :--- |
| **Operating System** | Mac: Click the Apple icon (top left) → About This Mac | macOS 12 (Monterey) or higher |
| | Linux: Run `cat /etc/os-release` in the terminal | Ubuntu 20.04+, Debian 11+, Fedora 36+, or similar |
| **Disk Space** | Mac: Apple icon → About This Mac → Storage | At least 2GB free |

---

## 🚀 Method 1: Official One-Line Install Script (Recommended)

The simplest way — one command handles everything.

### Step 1: Open the Terminal

**Mac users:**
- Press `Command (⌘) + Space` to open Spotlight
- Type `Terminal`
- Press Enter to open it

**Linux users:**
- Press `Ctrl + Alt + T` to open the terminal
- Or search for "Terminal" in your app launcher

### Step 2: Run the Install Command

Copy and paste the following command into the terminal and press **Enter**:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

The script will automatically:
1. Check if Node.js is installed (on Mac it will install Homebrew first if needed)
2. Install Node.js 22+ if missing or outdated
3. Install Git if needed
4. Install OpenClaw
5. Launch the setup wizard

> 💡 **Tip:** The whole process takes about 3-10 minutes depending on your internet speed and whether extra dependencies are needed.

### Step 3: Confirm the Installation

After installation, open a **new** terminal window and type:

```bash
openclaw --version
```

If you see a version number — you're good to go! 🎉

---

### ❓ Method 1: Common Issues

**Q: Mac shows a popup asking to install "Command Line Tools"?**
A: This is normal. Click **"Install"** and wait for it to finish (may take a few minutes). Then run the install command again.

**Q: It asks for a password during installation?**
A: This is your **computer login password** (not your Apple ID). The screen won't show any characters as you type — that's normal security behavior. Just type it and press Enter.

**Q: Installation seems stuck?**
A:
1. Press `Ctrl + C` to cancel
2. Check your internet connection
3. Try running the install command again

**Q: "openclaw: command not found"?**
A: Usually means PATH isn't configured correctly. See the [Can't Find openclaw Command](#cant-find-the-openclaw-command) section below.

**Q: Linux shows "Permission denied" or "EACCES"?**
A: This is an npm global install permissions issue. Fix it with:
```bash
mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
Then run the install command again.

---

## 🔧 Method 2: Manual Installation

If the one-line script didn't work, you can install step by step.

### Step 1: Install Node.js 22

**Mac users (via Homebrew):**

If you already have Homebrew (check with `brew --version`), run:

```bash
brew install node
```

If you don't have Homebrew, install it first:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then run `brew install node`.

> 💡 **Tip:** You can also download the Mac installer directly from [nodejs.org](https://nodejs.org).

**Linux users (Ubuntu / Debian):**

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Linux users (Fedora / RHEL):**

```bash
sudo dnf install nodejs
```

**Verify:** Open a new terminal and run `node -v`. You should see `v22.x.x` or higher.

---

### Step 2: Install OpenClaw

```bash
npm install -g openclaw@latest
```

> ⚠️ **"Permission denied" on Mac/Linux?** Add `sudo` before the command:
> ```bash
> sudo npm install -g openclaw@latest
> ```
> You'll be asked for your computer login password.

### Step 3: Start the Setup Wizard

```bash
openclaw onboard --install-daemon
```

---

## 🔧 Can't Find the openclaw Command?

### Quick Diagnosis

```bash
node -v
npm -v
npm prefix -g
echo "$PATH"
```

Check whether the path from `npm prefix -g` (e.g., `/usr/local/lib` or `/Users/yourname/.npm-global`) plus `/bin` appears in the `echo "$PATH"` output.

### Fix

If it's not in PATH, add it manually based on your shell:

**Mac (zsh, the default):**
```bash
echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Linux (bash, the default):**
```bash
echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Then try `openclaw --version` again.

---

## ✅ Quick Reference: Common Commands

| Command | What It Does |
| :--- | :--- |
| `openclaw --version` | Show OpenClaw version |
| `openclaw onboard` | Re-run the setup wizard |
| `openclaw dashboard` | Open the browser-based control panel |
| `openclaw doctor` | Auto-diagnose common issues |
| `openclaw gateway start` | Start the background service |
| `openclaw gateway stop` | Stop the background service |
| `openclaw gateway status` | Check background service status |
| `openclaw logs --follow` | View live logs |

---

## ❓ General FAQ

**Q: Installation succeeded — what's next?**
A: Run `openclaw onboard` to complete initial setup (choose your AI model, enter your API key, etc.). If you need help, tell me which step you're on.

**Q: Is the Node.js version from Homebrew up to date?**
A: Homebrew installs the latest LTS version. Run `node -v` to confirm it's 22.x or higher. If it's older, run `brew upgrade node`.

**Q: I have an M1/M2/M3/M4 Mac — any compatibility issues?**
A: None. OpenClaw fully supports Apple Silicon (M-series chips).

**Q: Can I install using Docker on Linux?**
A: Yes. OpenClaw provides Docker images, but for most personal users, a direct install is simpler. If you're comfortable with Docker and have specific needs, check the Docker section in the official docs.

---

## 🔒 Security Tips

- OpenClaw is cutting-edge experimental software — best used on a personal computer
- Never expose the gateway port to the public internet
- API keys are sensitive — don't share them
- You shouldn't need `sudo` for everyday use (only for installing global npm packages)

---

*Have questions? Tell me where you're stuck and I'll help you out.*
