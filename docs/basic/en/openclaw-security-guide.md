# OpenClaw Security Guide: Network Exposure & Port Safety

## TL;DR

**OpenClaw's gateway port is bound to localhost by default. It is NOT accessible from the internet or your local network.** No action needed unless you changed the configuration.

If you're worried, run this to confirm:

```bash
openclaw config show
```

Look for:
```
gateway.bind: "loopback"
```

If it says `"loopback"` — you're safe. The port (default 18789) only accepts connections from your own machine.

---

## What Is the Gateway Port?

OpenClaw runs a local gateway server (default port `18789`) that provides:
- The Control UI (web dashboard)
- WebSocket connections for the agent
- API endpoints for tools and plugins

This is the port that the agent, browser, and CLI all connect to. It's powerful — whoever can reach this port can control your agent, read files, and execute commands.

## Default Configuration: Safe

Out of the box, OpenClaw sets:

```json
{
  "gateway": {
    "port": 18789,
    "bind": "loopback",
    "auth": {
      "mode": "token"
    }
  }
}
```

- **`bind: "loopback"`** → Port listens on `127.0.0.1` only (localhost)
- **`auth.mode: "token"`** → Requires an auth token for all connections

This means:
- ✅ Only processes on your machine can connect
- ✅ Other devices on your WiFi/LAN **cannot** reach it
- ✅ The internet **cannot** reach it
- ✅ Even local connections need the auth token

## When Does It Become a Risk?

The port becomes externally accessible **only if you manually change** `gateway.bind` to `"all"`:

```json
{
  "gateway": {
    "bind": "all"  // ⚠️ DANGER — listens on all network interfaces
  }
}
```

With `bind: "all"`:
- The port listens on `0.0.0.0` (all interfaces)
- Any device on your local network can connect
- If your machine has a public IP (VPS, cloud server), **anyone on the internet** can connect
- Combined with a weak auth token, this is essentially remote code execution

### Common Ways People Accidentally Expose Themselves

1. **VPS/cloud deployment** — Setting `bind: "all"` to access the Control UI remotely, without a firewall
2. **Following bad advice** — Tutorials that say "set bind to all if you can't connect" without explaining the risk
3. **Router UPnP** — Some routers auto-forward ports, making LAN-bound services internet-accessible
4. **Copy-pasting configs** — Using someone else's `openclaw.json` without understanding every field

## How to Check Your Configuration

### Quick Check
```bash
openclaw config show
```

Look for the `gateway` section:
```
gateway.bind: "loopback"   ← ✅ Safe
gateway.bind: "all"        ← ⚠️ Exposed
```

### Full Security Audit
```bash
openclaw security audit
```

This runs a comprehensive check including:
- Port binding status
- Auth token strength
- File permissions
- Channel security
- Model tier warnings

### Network Check (Advanced)
```bash
# Linux/macOS — check what's listening on port 18789
lsof -i :18789
# or
ss -tlnp | grep 18789
# or
netstat -tlnp | grep 18789
```

You should see `127.0.0.1:18789` (safe), NOT `0.0.0.0:18789` (exposed).

On Windows:
```powershell
netstat -an | findstr 18789
```

## If You Need Remote Access (Do It Safely)

If you legitimately need to access OpenClaw from another device, **do NOT set `bind: "all"`**. Use one of these secure methods instead:

### Option 1: Tailscale (Recommended)
```json
{
  "gateway": {
    "bind": "loopback",
    "tailscale": {
      "mode": "on"
    }
  }
}
```
Tailscale creates an encrypted tunnel between your devices. No open ports, no firewall rules needed.

### Option 2: SSH Tunnel
Keep `bind: "loopback"` and tunnel from your remote machine:
```bash
ssh -L 18789:localhost:18789 user@your-server
```
Then access `http://localhost:18789` on your local machine.

### Option 3: Reverse Proxy with Auth
Put OpenClaw behind nginx or Caddy with:
- HTTPS/TLS termination
- Additional authentication (basic auth, OAuth, etc.)
- IP allowlisting

Keep `bind: "loopback"` and point the proxy to `127.0.0.1:18789`.

## Security Best Practices

1. **Keep `bind: "loopback"`** — Unless you have a specific reason and a secure tunnel
2. **Use a strong auth token** — At least 32 random characters
3. **Run `openclaw security audit`** regularly — It catches misconfigurations
4. **Don't share your `openclaw.json`** — It contains API keys and auth tokens
5. **Keep OpenClaw updated** — Security fixes are included in updates

## Summary

| Configuration | Localhost | LAN | Internet | Risk |
|---|---|---|---|---|
| `bind: "loopback"` (default) | ✅ Accessible | ❌ Blocked | ❌ Blocked | None |
| `bind: "all"` + firewall | ✅ Accessible | ✅ Accessible | ❌ Blocked | Low |
| `bind: "all"` + no firewall | ✅ Accessible | ✅ Accessible | ✅ Accessible | **Critical** |
| `bind: "all"` + Tailscale | ✅ Accessible | Via Tailscale | Via Tailscale | Low |

**Default is safe. Don't change it unless you know what you're doing.**
