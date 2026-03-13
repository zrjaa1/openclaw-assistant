# 微信（WeChat）接入配置指南

本指南将帮助你把 OpenClaw 连接到微信，让你的 AI 助手可以在微信里回复消息。

> ⚠️ **重要提示：** 微信的接入比飞书和钉钉**更复杂**。微信没有像飞书/钉钉那样的官方开放平台供个人开发者使用，所以需要通过一个"代理服务"来桥接。请做好多花一些时间的准备。

---

## ✅ 前置条件

- ✅ **OpenClaw 已安装并配置** — 运行 `openclaw doctor` 全绿
- ✅ **网关可以正常启动** — 运行 `openclaw gateway status` 看到 `running`
- ✅ **你有一个微信账号** — 用来登录代理服务（建议使用专门的微信号，不要用主号）

> ⚠️ **不确定基础配置是否完成？** 告诉我你的情况，我会先帮你搞定基础配置。

---

## 🤔 微信接入为什么比较特殊？

先解释一下为什么微信接入和飞书/钉钉不一样：

| 对比项 | 飞书/钉钉 | 微信 |
| :--- | :--- | :--- |
| **官方开放平台** | ✅ 有，支持个人开发者 | ❌ 微信公众平台对个人限制多 |
| **机器人 API** | ✅ 官方提供 | ❌ 没有个人可用的机器人 API |
| **接入方式** | 直接对接官方 API | 需要通过"代理服务"桥接 |
| **配置难度** | ⭐⭐ | ⭐⭐⭐⭐ |

因为微信不提供方便的开放 API，社区开发了代理服务来解决这个问题。代理服务会模拟微信客户端，把收到的消息转发给 OpenClaw。

---

## 📋 接入方案概览

目前有两个社区开发的微信插件可以选择：

| 插件 | 包名 | 特点 |
| :--- | :--- | :--- |
| **方案 A** | `@canghe/openclaw-wechat` | 更新频繁，维护活跃 |
| **方案 B** | `openclaw-wechat-channel` | 基于 Wechatify 代理 |

两个方案都需要搭配一个**微信代理服务**（proxy service）来使用。代理服务是一个独立运行的程序，它负责：
1. 登录你的微信账号
2. 接收微信消息
3. 把消息转发给 OpenClaw
4. 把 OpenClaw 的回复发回微信

> ⚠️ **注意：** 代理服务需要你登录微信账号。建议使用一个**专用的微信小号**，不要用你的主账号，以降低风险。

---

## 🚀 第一步：安装微信插件

在终端中运行（选一个方案即可）：

**方案 A（推荐）：**
```bash
openclaw plugins install @canghe/openclaw-wechat
```

**方案 B：**
```bash
openclaw plugins install openclaw-wechat-channel
```

---

## 📋 第二步：搭建微信代理服务

这是微信接入最关键也最复杂的一步。你需要运行一个代理服务来桥接微信和 OpenClaw。

> 💡 **提示：** 代理服务的具体搭建方式取决于你选择的方案和代理服务提供商。以下是通用的流程。

### 通用流程

**步骤 1：** 获取代理服务。常见的选择包括：
- 社区提供的开源代理服务
- 第三方微信代理 API 服务（部分需要付费）

**步骤 2：** 启动代理服务后，你会获得两个关键信息：
- **Proxy URL**：代理服务的地址（格式类似 `https://your-proxy-server.com`）
- **API Key**：用来验证身份的密钥（格式类似 `sk-open-xxx`）

**步骤 3：** 在代理服务中登录你的微信账号（通常通过扫码登录）。

> ⚠️ **安全提醒：**
> - 只使用你信任的代理服务
> - 建议使用专用微信小号
> - 不要把 API Key 分享给任何人

---

### ❓ 常见问题

**Q：代理服务在哪里获取？**
A：由于微信接入方案更新较快，建议查看插件的最新文档或在 [OpenClaw Discord 社区](https://discord.com/invite/clawd) 询问其他用户推荐的代理服务。

**Q：代理服务需要一直运行吗？**
A：是的。代理服务停止后，微信消息就无法转发给 OpenClaw 了。你可以把它部署在服务器上保持长期运行。

**Q：使用代理服务安全吗？**
A：代理服务需要访问你的微信账号，这确实存在一定风险。所以我们强烈建议使用专用小号，不要使用你的主微信账号。

---

## 🛠️ 第三步：配置 OpenClaw

拿到代理服务的 Proxy URL 和 API Key 后，配置 OpenClaw。

### 方式一：使用配置向导

```bash
openclaw channels add
```

选择 **WeChat**，然后按提示填入 Proxy URL 和 API Key。

### 方式二：编辑配置文件

编辑 `~/.openclaw/openclaw.json`：

**方案 A（`@canghe/openclaw-wechat`）：**
```json5
{
  "channels": {
    "openclaw-wechat": {
      "enabled": true,
      "apiKey": "sk-open-你的API Key",
      "proxyUrl": "https://your-proxy-server.com",
      "dmPolicy": "open"
    }
  }
}
```

**方案 B（`openclaw-wechat-channel`）：**
```json5
{
  "channels": {
    "wechat": {
      "enabled": true,
      "apiKey": "你的API Key",
      "proxyUrl": "https://your-proxy-server.com"
    }
  }
}
```

> ⚠️ **注意：** 把示例中的 URL 和 Key 换成你从代理服务获取的真实值。

---

### ❓ 常见问题

**Q：`dmPolicy` 应该设成什么？**
A：
- `"open"` — 所有人都可以和你的机器人聊天（最简单，但不太安全）
- `"allowlist"` — 只允许指定的人聊天（需要配置 `allowFrom` 列表）

如果你只是自己用，设成 `"open"` 最简单。如果要限制谁能使用：
```json5
{
  "channels": {
    "openclaw-wechat": {
      "enabled": true,
      "apiKey": "xxx",
      "proxyUrl": "xxx",
      "dmPolicy": "allowlist",
      "allowFrom": ["wxid_你的微信ID"]
    }
  }
}
```

---

## 🛠️ 第四步：启动并测试

**步骤 1：** 确认代理服务正在运行且已登录微信。

**步骤 2：** 重启 OpenClaw 网关：

```bash
openclaw gateway restart
```

**步骤 3：** 确认网关状态：

```bash
openclaw gateway status
```

**步骤 4：** 用另一个微信号给你的机器人微信号发一条消息，比如"你好"。

**步骤 5：** 如果一切正常，你应该能收到 AI 的回复！🎉

**步骤 6：** 运行体检确认：

```bash
openclaw doctor
```

---

### 查看实时日志

如果消息没有回复，查看日志排查：

```bash
openclaw logs --follow
```

---

### ❓ 常见问题

**Q：发消息后没有收到回复？**
A：按顺序检查：
1. 代理服务是否在运行？微信是否已登录？
2. `openclaw gateway status` — 网关是否在运行？
3. `openclaw logs --follow` — 日志里有没有报错？
4. Proxy URL 和 API Key 是否填写正确？
5. 代理服务的 webhook 是否指向了 OpenClaw？

**Q：代理服务掉线了怎么办？**
A：重新启动代理服务并重新登录微信。代理服务通常会提供自动重连功能，但微信登录状态可能需要重新扫码。

**Q：微信号被限制了怎么办？**
A：微信对自动发消息有风控机制。如果消息发送太频繁，可能会被临时限制。建议：
- 不要短时间内发送大量消息
- 使用有一定历史的微信号（新注册的号更容易被限制）
- 遇到限制后等待一段时间再试

---

## ❓ 综合常见问题

**Q：微信接入和飞书/钉钉接入比，优缺点是什么？**
A：

| 对比项 | 微信 | 飞书/钉钉 |
| :--- | :--- | :--- |
| **用户基数** | ⭐⭐⭐ 最大 | ⭐⭐ 企业用户为主 |
| **配置难度** | ⭐⭐⭐⭐ 较复杂 | ⭐⭐ 中等 |
| **稳定性** | ⭐⭐ 依赖代理服务 | ⭐⭐⭐ 官方 API 稳定 |
| **安全性** | ⭐⭐ 需要信任代理 | ⭐⭐⭐ 官方授权 |

如果你主要在企业场景使用，飞书或钉钉是更好的选择。如果你需要在微信上使用（比如和微信好友互动），那就需要微信方案。

**Q：两个微信插件选哪个？**
A：推荐方案 A（`@canghe/openclaw-wechat`），更新更频繁。但具体选择也取决于你使用的代理服务与哪个插件更兼容，建议在 OpenClaw 社区确认。

**Q：可以同时接入飞书和微信吗？**
A：完全可以！OpenClaw 支持同时连接多个通讯平台。每个平台独立配置，互不影响。

---

## 📋 快速命令参考表

| 命令 | 作用 |
| :--- | :--- |
| `openclaw plugins install @canghe/openclaw-wechat` | 安装微信插件 |
| `openclaw channels add` | 配置向导 |
| `openclaw gateway restart` | 重启网关 |
| `openclaw gateway status` | 查看网关状态 |
| `openclaw logs --follow` | 实时查看日志 |
| `openclaw doctor` | 全面体检 |

---

*微信接入比较复杂，遇到问题别着急。把你看到的错误信息告诉我，我来帮你排查。也欢迎加入 [OpenClaw Discord 社区](https://discord.com/invite/clawd) 交流。*
