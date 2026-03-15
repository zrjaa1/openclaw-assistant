# OpenClaw Uninstall Guide

If you want to completely remove OpenClaw, follow the steps below. Uninstalling won't affect any other software on your computer.

---

## The Easy Way (Recommended)

If the `openclaw` command still works, one command handles everything:

Copy and paste this into your terminal:
```
openclaw uninstall
```

It will ask a few confirmation questions — just follow the prompts.

To skip all confirmations and remove everything at once:
```
openclaw uninstall --all --yes
```

---

## Manual Uninstall Steps

If the command above doesn't work, you can uninstall step by step:

### 1. Stop the Background Service

```
openclaw gateway stop
openclaw gateway uninstall
```

### 2. Delete Config and Data

**Windows:**
Open File Explorer, type `%USERPROFILE%\.openclaw` in the address bar, press Enter, then delete the entire folder.

**Mac/Linux:**
```
rm -rf ~/.openclaw
```

### 3. Remove the Program

```
npm rm -g openclaw
```

---

## Windows: Extra Cleanup

If the background service is still running after uninstall, manually remove the scheduled task:

Press `Win + X` → open PowerShell (Admin), then run:
```
schtasks /Delete /F /TN "OpenClaw Gateway"
```

---

## Mac: Extra Cleanup

If the background service is still running after uninstall:

```
launchctl bootout gui/$UID/ai.openclaw.gateway
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

If you installed the macOS desktop app, remove it too:
```
rm -rf /Applications/OpenClaw.app
```

---

## Linux: Extra Cleanup

If the background service is still running after uninstall:

```
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

---

## FAQ

**Q: Can I reinstall after uninstalling?**
A: Of course! Reinstall anytime, just like the first time. Previous config will be gone — you'll need to set up again.

**Q: Will uninstalling affect other software on my computer?**
A: No. Uninstalling only removes OpenClaw's own files — it won't touch anything else.

**Q: I want to keep my config and just update the program — is that possible?**
A: Yes! You don't need to uninstall for that. See the Update Guide instead.

**Q: Should I uninstall Node.js too?**
A: No need. Node.js is independent software that other programs may also use. If you're sure you don't need it, you can uninstall Node.js separately, but that's unrelated to OpenClaw's uninstall.

---

*Hit a problem during uninstall? Share the error message from your terminal and I'll help you fix it.*
