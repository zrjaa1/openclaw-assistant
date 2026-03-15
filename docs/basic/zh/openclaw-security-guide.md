# OpenClaw 安全指南：网络暴露与端口安全

## 快速总结

**OpenClaw 的网关端口默认绑定到 localhost，不会被外部网络访问。** 除非你手动修改了配置，否则无需担心。

如果你想确认，运行：

```bash
openclaw config show
```

查看：
```
gateway.bind: "loopback"
```

如果显示 `"loopback"` — 你是安全的。端口（默认 18789）只接受本机连接。

---

## 网关端口是什么？

OpenClaw 运行一个本地网关服务器（默认端口 `18789`），提供：
- 控制台 UI（Web 仪表板）
- WebSocket 连接（用于 Agent）
- 工具和插件的 API 接口

这个端口功能强大 — 任何能访问这个端口的人，都可以控制你的 Agent、读取文件、执行命令。

## 默认配置：安全

开箱即用的配置：

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

- **`bind: "loopback"`** → 端口仅监听 `127.0.0.1`（本机）
- **`auth.mode: "token"`** → 所有连接需要认证令牌

这意味着：
- ✅ 只有本机进程能连接
- ✅ 同一 WiFi/局域网的其他设备**无法**访问
- ✅ 互联网**无法**访问
- ✅ 即使本地连接也需要认证令牌

## 什么时候会有风险？

端口只有在你**手动修改** `gateway.bind` 为 `"all"` 时才会暴露：

```json
{
  "gateway": {
    "bind": "all"  // ⚠️ 危险 — 监听所有网络接口
  }
}
```

设置 `bind: "all"` 后：
- 端口监听 `0.0.0.0`（所有接口）
- 局域网中的任何设备都能连接
- 如果你的机器有公网 IP（VPS、云服务器），**任何人都能连接**
- 配合弱认证令牌，等于远程代码执行漏洞

### 常见的意外暴露方式

1. **VPS/云部署** — 为了远程访问控制台设置 `bind: "all"`，但没有配置防火墙
2. **跟着不靠谱的教程** — "连不上就设置 bind 为 all"，但没解释风险
3. **路由器 UPnP** — 某些路由器会自动转发端口
4. **复制别人的配置** — 不理解每个字段的含义

## 如何检查你的配置

### 快速检查
```bash
openclaw config show
```

查看 `gateway` 部分：
```
gateway.bind: "loopback"   ← ✅ 安全
gateway.bind: "all"        ← ⚠️ 暴露
```

### 完整安全审计
```bash
openclaw security audit
```

### 网络检查（进阶）
```bash
# Linux/macOS — 检查端口 18789 的监听状态
lsof -i :18789
# 或
ss -tlnp | grep 18789
```

应该看到 `127.0.0.1:18789`（安全），而不是 `0.0.0.0:18789`（暴露）。

Windows：
```powershell
netstat -an | findstr 18789
```

## 如果需要远程访问（安全的方式）

如果确实需要从其他设备访问 OpenClaw，**不要设置 `bind: "all"`**。使用以下安全方法：

### 方法 1：Tailscale（推荐）
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
Tailscale 在设备之间创建加密隧道，无需开放端口。

### 方法 2：SSH 隧道
保持 `bind: "loopback"`，从远程机器建立隧道：
```bash
ssh -L 18789:localhost:18789 user@your-server
```
然后在本地访问 `http://localhost:18789`。

### 方法 3：反向代理 + 认证
用 nginx 或 Caddy 反向代理，配置：
- HTTPS/TLS
- 额外认证（基本认证、OAuth 等）
- IP 白名单

保持 `bind: "loopback"`，代理指向 `127.0.0.1:18789`。

## 安全最佳实践

1. **保持 `bind: "loopback"`** — 除非有特定需求并使用安全隧道
2. **使用强认证令牌** — 至少 32 个随机字符
3. **定期运行 `openclaw security audit`** — 检测配置问题
4. **不要分享 `openclaw.json`** — 包含 API 密钥和认证令牌
5. **保持 OpenClaw 更新** — 包含安全修复

## 总结

| 配置 | 本机 | 局域网 | 互联网 | 风险 |
|---|---|---|---|---|
| `bind: "loopback"`（默认） | ✅ 可访问 | ❌ 不可访问 | ❌ 不可访问 | 无 |
| `bind: "all"` + 防火墙 | ✅ 可访问 | ✅ 可访问 | ❌ 不可访问 | 低 |
| `bind: "all"` + 无防火墙 | ✅ 可访问 | ✅ 可访问 | ✅ 可访问 | **严重** |
| `bind: "all"` + Tailscale | ✅ 可访问 | 通过 Tailscale | 通过 Tailscale | 低 |

**默认配置是安全的。不懂就别改。**
