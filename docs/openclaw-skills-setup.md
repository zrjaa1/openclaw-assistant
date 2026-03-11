# OpenClaw 技能（Skills）入门指南

OpenClaw 的"技能"就像给 AI 助手安装的"应用"——让它学会新本领。比如控制智能灯光、查看天气、管理笔记等等。本指南帮你了解技能的基本概念，并安装你的第一个技能。

> 💡 **提示：** 技能是可选的增强功能。即使不安装任何技能，OpenClaw 也能正常聊天。当你需要 AI 助手做更多事情时，再来安装技能。

---

## ✅ 前置条件

- ✅ **OpenClaw 已安装并配置** — 运行 `openclaw doctor` 全绿
- ✅ **网关正在运行** — 运行 `openclaw gateway status` 看到 `running`

> ⚠️ **还没完成基础配置？** 请先完成初始化配置（选择 AI 模型、填入 API Key），确认 `openclaw doctor` 全绿后再回来。

---

## 🤔 什么是技能？

简单来说：

| 概念 | 类比 | 说明 |
| :--- | :--- | :--- |
| **OpenClaw 本体** | 手机 | 基础的 AI 对话平台 |
| **技能 (Skills)** | 手机上的 App | 给 AI 助手增加新功能 |
| **插件 (Plugins)** | 手机的通信模块 | 连接新的聊天平台（飞书、钉钉等） |

**技能 vs 插件的区别：**
- **插件**是让 OpenClaw 连接到新的聊天平台（飞书、钉钉、微信等）
- **技能**是让 AI 助手学会新的能力（查天气、控制灯光、搜索网页等）

> 💡 **提示：** OpenClaw 安装时已经自带了一些基础技能。你可以随时查看和添加更多。

---

## 🚀 第一步：查看已有技能

打开终端，运行：

```bash
openclaw skills list
```

这会列出所有可用的技能。你会看到：
- ✅ **已激活**的技能（满足所有条件，已加载）
- ⚠️ **未激活**的技能（缺少某些条件，比如需要安装额外工具或配置 API Key）

想看某个技能的详细信息：

```bash
openclaw skills info <技能名称>
```

比如查看天气技能：

```bash
openclaw skills info weather
```

---

### ❓ 常见问题

**Q：列表里的技能太多了，怎么只看已激活的？**
A：运行 `openclaw skills list --eligible`，只显示已经满足条件、可以使用的技能。

**Q：技能列表是空的？**
A：正常情况下不会为空。运行 `openclaw skills check` 来诊断技能加载状态。

---

## 📋 第二步：安装新技能

有两种方式安装技能：

### 方式一：从 ClawHub 安装（推荐）

ClawHub 是 OpenClaw 的技能商店，你可以在那里浏览和安装社区开发的技能。

**浏览技能：** 打开浏览器访问 [https://clawhub.com](https://clawhub.com)

**安装技能：** 在终端中运行（把 `<技能名称>` 换成你想安装的）：

```bash
clawhub install <技能名称>
```

### 方式二：手动安装

如果你知道技能的 npm 包名，也可以直接安装：

```bash
openclaw plugins install <包名>
```

> 💡 **提示：** 大部分用户用方式一（ClawHub）就够了，简单直观。

---

### ❓ 常见问题

**Q：`clawhub` 命令找不到？**
A：ClawHub CLI 可能需要单独安装：
```bash
npm install -g clawhub
```

**Q：安装技能后需要重启 OpenClaw 吗？**
A：不需要。OpenClaw 会自动检测新安装的技能并在下一次对话中加载。

---

## 🛠️ 第三步：配置技能

有些技能安装后就能直接用（比如天气查询），有些需要额外配置（比如需要填入第三方服务的 API Key）。

### 查看技能是否需要配置

```bash
openclaw skills info <技能名称>
```

如果输出中提到需要 API Key 或环境变量，你需要在配置文件中添加：

```json5
// ~/.openclaw/openclaw.json
{
  "skills": {
    "entries": {
      "技能名称": {
        "enabled": true,
        "env": {
          "SOME_API_KEY": "你的密钥"
        }
      }
    }
  }
}
```

### 启用/禁用技能

如果你想关闭某个技能：

```json5
{
  "skills": {
    "entries": {
      "某个技能": {
        "enabled": false
      }
    }
  }
}
```

---

### ❓ 常见问题

**Q：配置文件在哪里？**
A：`~/.openclaw/openclaw.json`
- Mac/Linux：终端输入 `open ~/.openclaw`（Mac）或 `xdg-open ~/.openclaw`（Linux）
- Windows：在文件资源管理器地址栏输入 `%USERPROFILE%\.openclaw`

**Q：修改配置后怎么生效？**
A：技能配置修改后，会在下一个新对话中自动生效。如果你想立刻生效，可以重启网关：
```bash
openclaw gateway restart
```

**Q：JSON 格式写错了会怎样？**
A：OpenClaw 启动时会报错，告诉你配置文件哪里有问题。按照提示修改即可。如果不确定 JSON 格式是否正确，可以把内容复制到在线 JSON 检查工具（比如 [jsonlint.com](https://jsonlint.com)）验证。

---

## 📋 新手推荐技能

以下是一些适合新手的实用技能，安装后无需额外配置就能使用：

| 技能 | 功能 | 安装命令 |
| :--- | :--- | :--- |
| **weather** | 查询天气和天气预报 | 内置，无需安装 |
| **web-search** | 搜索网页（需要搜索引擎配置） | 内置，需配置搜索引擎 |

> 💡 **提示：** 更多技能请浏览 [clawhub.com](https://clawhub.com)。社区不断在开发新技能！

---

## 📋 常用命令速查

| 命令 | 作用 |
| :--- | :--- |
| `openclaw skills list` | 列出所有技能 |
| `openclaw skills list --eligible` | 只看已激活的技能 |
| `openclaw skills info <名称>` | 查看技能详情 |
| `openclaw skills check` | 诊断技能加载状态 |
| `clawhub install <名称>` | 从 ClawHub 安装技能 |
| `openclaw plugins list` | 列出所有插件 |
| `openclaw plugins install <包名>` | 安装插件 |

---

## ❓ 综合常见问题

**Q：技能和插件有什么关系？**
A：它们是不同的东西：
- **技能** = AI 助手的能力（查天气、控灯、搜索等）
- **插件** = 连接聊天平台的通道（飞书、钉钉等）
两者可以独立安装和使用。

**Q：安装太多技能会不会让 AI 变慢？**
A：每个技能会占用一小部分 AI 的"注意力"（上下文窗口），但通常影响可以忽略。如果你确实发现响应变慢了，可以禁用不常用的技能。

**Q：技能会自动更新吗？**
A：不会。你可以手动更新：
```bash
clawhub update --all
```

**Q：我可以自己开发技能吗？**
A：可以！技能本质上是一个包含 `SKILL.md` 文件的文件夹。OpenClaw 官方文档有详细的开发指南，适合有一定技术基础的用户。

**Q：安装技能安全吗？**
A：ClawHub 上的技能由社区维护。和安装任何第三方软件一样，建议只安装你信任的技能。OpenClaw 会在安装时做基本的安全检查。

---

*有问题？欢迎加入 [OpenClaw Discord 社区](https://discord.com/invite/clawd) 提问。*
