# OpenClaw Windows Installation Guide

This guide will help you install OpenClaw on a Windows computer. We'll explain every step in detail — don't panic if you run into problems, most of them have straightforward solutions.

---

## ✅ Before You Start: Check Your System

Make sure your computer meets these requirements:

| Requirement | How to Check | Minimum |
| :--- | :--- | :--- |
| **Operating System** | Press `Win + I` → System → About | Windows 10 (64-bit) or Windows 11 |
| **System Type** | Same place, look for "System type" | Must be **64-bit operating system** |
| **Disk Space** | Open "This PC" and check your C: drive | At least 2GB free |

> ⚠️ **Unsupported systems:** If your computer runs Windows 7, Windows 8/8.1, or is a 32-bit system, OpenClaw unfortunately cannot run on it. You'll need to upgrade to Windows 10 or 11 first.

> 💡 **Tip:** Not sure what version you have? Press `Win + R`, type `winver`, press Enter — a window will show your Windows version.

---

## 🚀 Method 1: Official One-Line Install Script (Recommended)

The simplest way — the script automatically detects your environment, installs dependencies, and sets up OpenClaw.

### Step 1: Open PowerShell

1. Hold the `Win` key (bottom-left of keyboard, has the Windows logo) and press `X`
2. In the popup menu, click **Windows PowerShell** or **Terminal**
3. A dark command-line window will appear

> 💡 **Tip:** If you don't see a PowerShell option in the menu, click the Start menu, search for `PowerShell`, and open it.

> ⚠️ **Note:** You do NOT need to run as Administrator for this step. Regular mode is fine.

### Step 2: Run the Install Command

Copy the following command:

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Then **right-click** in the PowerShell window to paste (right-click = paste in PowerShell) and press **Enter**.

> 💡 **Tip:** If nothing seems to happen after pasting, don't worry — just wait. The install process needs to download files from the internet, which may take a few minutes.

The script will automatically:
1. Check if Node.js is installed (OpenClaw's runtime environment)
2. Install Node.js 22 if it's missing
3. Install OpenClaw
4. Launch the setup wizard

### Step 3: Confirm the Installation

After installation, **close the current PowerShell window and open a new one** (this is important — the new window is needed to recognize newly installed commands). Then type:

```powershell
openclaw --version
```

If you see a version number (like `1.x.x`), congratulations — installation is complete! 🎉

---

### ❓ Method 1: Common Issues

**Q: It says "cannot be loaded", "execution policy", or "is not digitally signed"?**
A: This is a default Windows security restriction. To fix it:
1. Close the current PowerShell window
2. Click the Start menu, search for `PowerShell`
3. **Right-click** PowerShell and select **"Run as Administrator"**
4. In the admin window, type the following command. When prompted, type `Y` and press Enter:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
5. Close the admin window
6. Open a **regular** (non-admin) PowerShell and re-run the install command

> ⚠️ **Note:** You only need to change the execution policy once. Future installs won't need this step.

**Q: Installation seems stuck — the progress bar isn't moving?**
A: Likely a network issue.
1. Press `Ctrl + C` to cancel
2. Check your internet connection
3. Try running the install command again

**Q: It says "npm error spawn git ENOENT" or can't find git?**
A: You need to install Git first. Open your browser, go to [https://git-scm.com/downloads/win](https://git-scm.com/downloads/win), download and install it (just click "Next" through everything). After installing Git, **close PowerShell and open a new one**, then re-run the install command.

**Q: It says "openclaw is not recognized as an internal or external command"?**
A: This usually means PATH isn't configured correctly. See the [Can't Find openclaw Command](#cant-find-the-openclaw-command) section below.

---

## 🔧 Method 2: Manual Step-by-Step Installation

If the one-line script didn't work, you can install everything manually.

### Step 1: Install Node.js 22

OpenClaw requires Node.js 22 or higher. Choose one of these methods:

**Option A: Using winget (simplest, built into Windows 10 1709+)**

Open PowerShell and type:

```powershell
winget install OpenJS.NodeJS.LTS
```

> 💡 **Tip:** `winget` is Windows' built-in package manager. If it says `winget is not recognized`, your Windows version is too old — use Option B instead.

**Option B: Download from the official website**

1. Open your browser and go to [https://nodejs.org](https://nodejs.org)
2. Click the **LTS (Long Term Support)** download button (make sure the version is 22.x or higher)
3. Run the downloaded installer
4. Click **"Next"** through every step — no need to change any options
5. Click **"Finish"** to complete

> ⚠️ **Important:** After installing, you **must close all PowerShell windows and open a new one** — otherwise the system won't recognize the newly installed Node.js.

**Verify:** Open a brand new PowerShell window and type:

```powershell
node -v
```

If you see `v22.x.x` or higher, Node.js is installed successfully.

---

### Step 2: Install Git

Some OpenClaw dependencies need Git. If you don't have it:

1. Open your browser and go to [https://git-scm.com/downloads/win](https://git-scm.com/downloads/win)
2. Download and install — **keep all default options**, just click "Next" until done

> 💡 **Tip:** Not sure if Git is already installed? Open PowerShell and type `git --version`. If you see a version number, you already have it — skip this step.

---

### Step 3: Install OpenClaw

In PowerShell, copy and paste this command and press Enter:

```powershell
npm install -g openclaw@latest
```

> 💡 **Tip:** Installation may take 2-5 minutes depending on your internet speed. If you see some `WARN` warnings, those are usually fine to ignore. As long as there are no `ERR!` errors at the end, the install succeeded.

---

### Step 4: Verify Installation

Close PowerShell, open a new one, and type:

```powershell
openclaw --version
```

If you see a version number — installation is complete! 🎉 Now run the setup wizard:

```powershell
openclaw onboard --install-daemon
```

> 💡 **Tip:** The `--install-daemon` flag installs OpenClaw as a background service, so it keeps running even after you close PowerShell.

---

## 🛠️ Method 3: Using WSL2 (Recommended for Advanced Users)

If you have some technical experience, OpenClaw **strongly recommends** using WSL2 (Windows Subsystem for Linux) on Windows. WSL2 has better compatibility and fewer issues.

> 💡 **Tip:** If you don't know what WSL is or this sounds complicated, skip this method and use Method 1 or 2 instead.

### Step 1: Install WSL2

Open PowerShell **as Administrator** (right-click → Run as Administrator) and type:

```powershell
wsl --install
```

This will install WSL2 and Ubuntu. You'll **need to restart your computer** when it's done.

### Step 2: Set Up Ubuntu

After restarting, search for `Ubuntu` in the Start menu and open it. First launch will ask you to set a username and password (this is for the Linux system, separate from your Windows login).

### Step 3: Install OpenClaw in WSL2

In the Ubuntu terminal, run:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

The rest of the setup is identical to a regular Linux installation.

---

## 🔧 Can't Find the openclaw Command?

This is one of the most common issues on Windows. It usually means the path where npm installs commands hasn't been added to your system's PATH.

### Quick Diagnosis

Open a new PowerShell window and run these three commands:

```powershell
node -v
npm -v
npm prefix -g
```

**Case 1:** `node -v` or `npm -v` gives an error
→ Node.js isn't installed properly — go back and reinstall it

**Case 2:** First two work, `npm prefix -g` shows a path (like `C:\Users\YourName\AppData\Roaming\npm`)
→ You need to add that path to PATH. Follow the steps below:

### Adding to PATH Manually

1. Press `Win + I` to open Windows Settings
2. Search for **"environment variables"** and click **"Edit the system environment variables"**
3. In the popup window, click the **"Environment Variables"** button at the bottom
4. In the **top section** ("User variables"), find `Path` and double-click it
5. Click **"New"** and paste the path from the `npm prefix -g` command
6. Click **"OK"** to save all windows
7. **Close all PowerShell windows and open a new one**
8. Run `openclaw --version` to verify

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

**Q: My computer isn't very powerful — will OpenClaw be slow?**
A: OpenClaw itself uses very few resources (it's essentially a message relay). AI processing happens in the cloud, so your computer's specs have minimal impact on performance.

**Q: Do I need to disable antivirus software?**
A: Normally no. But if your antivirus blocks something during installation, you can click "Allow" or temporarily disable real-time protection, then re-enable it after installation.

**Q: My work computer has IT restrictions — can I still install?**
A: If your company's IT policies restrict software installation, you may need to contact IT for permission. Common restrictions include:
- PowerShell scripts blocked → IT needs to change the execution policy
- Global npm installs blocked → IT needs to grant npm permissions
- Proxy/firewall blocking downloads → IT needs to whitelist the URLs
If your company doesn't allow it, consider using OpenClaw on a personal computer instead.

**Q: Can I uninstall Node.js after OpenClaw is set up?**
A: No. Node.js is OpenClaw's runtime — removing it will break OpenClaw.

---

## 🔒 Security Tips

- OpenClaw is cutting-edge experimental software — best used on a personal computer
- You should NOT need to run as Administrator during everyday use (only for changing the execution policy)
- Never expose the gateway port to the public internet
- API keys are sensitive — don't share them
