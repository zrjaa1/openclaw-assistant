# 钉钉（DingTalk）接入配置指南

本指南将带你一步步完成 OpenClaw 与钉钉的连接配置，让你的 AI 助手在钉钉里随时响应消息。

> 💡 **提示：** 钉钉接入使用的是社区开发的插件 `@adongguo/openclaw-dingtalk`，功能完善，支持私聊和群聊。

---

## ✅ 前置条件（开始之前请确认）

- ✅ **OpenClaw 已安装** — 在终端输入 `openclaw --version`，能看到版本号
- ✅ **大模型已配置** — 运行 `openclaw doctor`，结果全绿（没有红色 ✗）
- ✅ **网关可以正常启动** — 运行 `openclaw gateway`，没有报错
- ✅ **你有钉钉企业管理员权限** — 或者能联系管理员帮你操作

> ⚠️ **不确定怎么做？** 直接告诉我你的情况，我会先帮你搞定基础配置。

---

## 🚀 第一步：安装钉钉插件

打开你的命令行窗口（Windows 用 PowerShell，Mac/Linux 用终端），输入：

```bash
openclaw plugins install @adongguo/openclaw-dingtalk
```

安装完成后，运行以下命令确认插件已生效：

```bash
openclaw gateway status
```

---

### ❓ 常见问题

**Q：安装时报错 "npm ERR!" 怎么办？**
A：先确认 Node.js 版本 >= 22（运行 `node -v` 检查）。如果版本没问题但还是报错，尝试用国内镜像安装：
```bash
npm install -g @adongguo/openclaw-dingtalk --registry=https://registry.npmmirror.com
```

---

## 📋 第二步：创建钉钉应用

和飞书类似，钉钉机器人也需要通过"企业内部应用"的方式接入。

### 操作步骤

**步骤 1：** 打开浏览器，访问钉钉开放平台：[https://open-dev.dingtalk.com](https://open-dev.dingtalk.com)

用你的钉钉账号登录。

**步骤 2：** 进入 **"应用开发"** → **"企业内部开发"**，点击 **"创建应用"**。

> ⚠️ **注意：** 你需要有企业管理员权限才能创建应用。如果没有权限，请联系你的钉钉企业管理员。

**步骤 3：** 填写应用信息：
- **应用名称**：随便起，比如 "AI 助手"
- **应用描述**：可以写 "OpenClaw AI 机器人"
- **应用图标**：上传一张图片，或跳过

**步骤 4：** 点击 **"确认创建"**。

**步骤 5：** 进入应用后，在 **"基础信息"** → **"应用信息"** 中，找到并复制：

- **AppKey (ClientID)**：格式类似 `dingxxxxxxxx`
- **AppSecret (ClientSecret)**：一串密钥

> ⚠️ **注意：** AppSecret 相当于密码，**不要分享给任何人**。如果不小心泄露了，请立刻在同一页面重置。

**步骤 6：** 把 AppKey 和 AppSecret 复制保存好，后面要用。

---

### ❓ 常见问题

**Q：找不到"企业内部开发"入口？**
A：钉钉开放平台界面可能有版本差异。登录后在左侧菜单找"应用开发"，然后点"企业内部应用"或"内部开发"。如果还是找不到，试试直接访问 [https://open-dev.dingtalk.com/console/app/create](https://open-dev.dingtalk.com/console/app/create)。

**Q：提示"没有权限创建应用"？**
A：联系你的钉钉企业管理员，让他在"管理后台 → 应用管理"里给你开发者权限，或者让管理员帮你创建应用。

---

## 📋 第三步：开启机器人能力

### 操作步骤

**步骤 1：** 在应用页面，找到 **"应用功能"** 或 **"应用能力"**。

**步骤 2：** 找到 **"机器人"** 选项，点击 **"开启"**。

**步骤 3：** 在机器人配置中，选择连接模式为 **"Stream 模式"**。

> 💡 **提示：** 一定要选 **Stream 模式**，不要选 HTTP 模式。Stream 模式不需要公网服务器，家庭网络就能用。

**步骤 4：** 设置机器人名称（这是用户在钉钉里看到的名字）。

**步骤 5：** 点击 **"保存"** 或 **"发布"**。

---

### ❓ 常见问题

**Q：没有看到 "Stream 模式" 选项？**
A：可能是钉钉版本较旧。尝试在机器人配置页面找"消息接收模式"，选择"Stream"或"长连接"。如果完全没有这个选项，可能需要更新钉钉开放平台。

---

## 📋 第四步：发布应用

应用创建后需要发布才能使用。

### 操作步骤

**步骤 1：** 在应用页面，找到 **"版本管理与发布"** 或 **"应用发布"**。

**步骤 2：** 点击 **"创建版本"**，填写版本号（比如 `1.0.0`）和更新说明。

**步骤 3：** 点击 **"发布"**。

> 💡 **提示：** 你可以先发布到"测试版本"来测试。测试版本只有你自己能看到机器人，确认没问题后再发布正式版。

**步骤 4：** 等待审核通过。企业内部应用通常很快就能通过（管理员在管理后台审批）。

---

### ❓ 常见问题

**Q：发布后在钉钉里搜不到机器人？**
A：
1. 确认应用已经通过审批
2. 确认你的账号在应用的"可用范围"内（应用设置里可以查看）
3. 在钉钉搜索框里搜索机器人名称
4. 如果只发布了测试版本，只有被添加为测试人员的账号才能看到

---

## 🛠️ 第五步：配置 OpenClaw

现在把 AppKey 和 AppSecret 填进 OpenClaw。

### 方式一：使用命令行配置（推荐）

在终端中依次运行以下三条命令（把引号里的内容换成你自己的值）：

```bash
openclaw config set channels.dingtalk.appKey "dingXXXXXXXX"
openclaw config set channels.dingtalk.appSecret "你的AppSecret"
openclaw config set channels.dingtalk.enabled true
```

### 方式二：直接编辑配置文件

配置文件位于 `~/.openclaw/openclaw.json`，添加 `channels.dingtalk` 部分：

```json5
{
  "channels": {
    "dingtalk": {
      "enabled": true,
      "appKey": "dingXXXXXXXX",
      "appSecret": "你的AppSecret",
      "connectionMode": "stream",
      "dmPolicy": "pairing",
      "requireMention": true
    }
  }
}
```

两种配置方式的对比：

| 特性 | 命令行配置 | 编辑配置文件 |
| :--- | :--- | :--- |
| **难度** | ⭐ 简单，复制粘贴 | ⭐⭐ 需要了解 JSON 格式 |
| **适合人群** | 所有人 | 需要高级配置时 |
| **出错风险** | 低 | JSON 格式写错会报错 |

> ⚠️ **注意：** 把 `dingXXXXXXXX` 和 `你的AppSecret` 换成你在第二步拿到的真实值，不要照抄示例。

---

### ❓ 常见问题

**Q：配置文件在哪里？**
A：
- Mac/Linux：`~/.openclaw/openclaw.json`（在终端输入 `open ~/.openclaw` 可以打开文件夹）
- Windows：`%USERPROFILE%\.openclaw\openclaw.json`（在文件资源管理器地址栏输入 `%USERPROFILE%\.openclaw`）

---

## 🛠️ 第六步：启动并测试

### 操作步骤

**步骤 1：** 启动（或重启）OpenClaw 网关：

```bash
openclaw gateway restart
```

**步骤 2：** 确认网关状态：

```bash
openclaw gateway status
```

看到 `running` 字样说明正常。

**步骤 3：** 打开钉钉，搜索你的机器人名字，点开对话框。

**步骤 4：** 发一条消息，比如"你好"。

**步骤 5：** 机器人会回复一个**配对码**（pairing code）。这是安全验证步骤。

**步骤 6：** 回到终端，输入以下命令批准配对（把配对码换成你收到的实际值）：

```bash
openclaw pairing approve dingtalk XXXXXX
```

**步骤 7：** 配对成功后，再发一条消息，机器人就会正常回复了！🎉

**步骤 8：** 运行全面体检，确认一切正常：

```bash
openclaw doctor
```

看到钉钉相关的检查项全绿就说明配置完美！

---

### 查看实时日志

如果机器人没反应，用以下命令排查：

```bash
openclaw logs --follow
```

按 `Ctrl+C` 退出日志查看。

---

### ❓ 常见问题

**Q：发消息后机器人没有任何反应？**
A：按顺序检查：
1. `openclaw gateway status` — 网关是否在运行？
2. `openclaw logs --follow` — 日志里有没有报错？
3. 应用是否已发布并通过审核？（第四步）
4. 机器人能力是否开启了 **Stream 模式**？（第三步）
5. AppKey 和 AppSecret 是否正确？（重新检查第二步）

**Q：配对码过期了怎么办？**
A：在钉钉里重新给机器人发一条消息，会收到新的配对码，然后立刻去终端批准。

**Q：不想每次都配对，能不能自动允许所有人？**
A：可以把配置中的 `dmPolicy` 改为 `"open"`。但要注意，这意味着任何能找到你机器人的人都可以使用它。更安全的做法是配对后就一直保持连接。

---

## 📋 第七步：群聊配置（可选）

如果你想让机器人在钉钉群里也能使用：

### 把机器人添加到群聊

**步骤 1：** 打开目标群聊，点击右上角的群设置。

**步骤 2：** 找到 **"智能群助手"** 或 **"群机器人"**，点击添加。

**步骤 3：** 在列表中找到你的机器人，添加进群。

### 群聊 @mention 行为

机器人在群聊里默认**只响应 @它 的消息**（不会对每条消息都回复）。

| 配置 | 效果 |
| :--- | :--- |
| 默认（`requireMention: true`） | 必须 @机器人 才会回复 |
| `requireMention: false` | 群里所有消息都触发机器人 |

如果你想让某个群不需要 @mention：

```json5
{
  "channels": {
    "dingtalk": {
      "requireMention": false
    }
  }
}
```

### 群聊访问控制

| 策略 | 配置值 | 效果 |
| :--- | :--- | :--- |
| 只允许指定群（默认） | `groupPolicy: "allowlist"` | 需要手动加白名单 |
| 所有群都可以用 | `groupPolicy: "open"` | 添加了机器人的群都能用 |
| 完全禁用群聊 | `groupPolicy: "disabled"` | 机器人在所有群都不响应 |

> 💡 **提示：** 如果你想让所有群都可以使用机器人，把 `groupPolicy` 改为 `"open"`。

---

### ❓ 常见问题

**Q：群里 @机器人 没反应？**
A：
1. 确认机器人已成功加入群（群设置里能看到）
2. @mention 时要用钉钉的 @功能（输入 @ 后从列表选择机器人），不是手动打名字
3. 确认 `groupPolicy` 不是 `"disabled"`
4. 查看日志：`openclaw logs --follow`

---

## ❓ 综合常见问题

**Q：钉钉和飞书的配置有什么区别？**
A：主要区别：

| 对比项 | 钉钉 | 飞书 |
| :--- | :--- | :--- |
| **开放平台** | open-dev.dingtalk.com | open.feishu.cn |
| **插件** | 社区插件 `@adongguo/openclaw-dingtalk` | 官方内置 |
| **凭证名称** | AppKey + AppSecret | App ID + App Secret |
| **连接模式** | Stream 模式 | 长连接模式 |
| **配置方式** | `openclaw config set` 或编辑配置文件 | `openclaw channels add` 向导或编辑配置文件 |

操作流程基本相同：创建应用 → 获取凭证 → 开启机器人 → 配置 OpenClaw → 测试。

**Q：消息回复为什么不是流式（打字机效果）？**
A：这是钉钉 API 的限制。钉钉的消息更新接口有频率限制，流式输出容易触发限流。所以插件采用"等 AI 回复完成后一次性发送"的方式，确保稳定性。

**Q：可以编辑已发送的消息吗？**
A：不可以，这是钉钉平台的限制。机器人无法修改已发送的消息。

**Q：AppSecret 泄露了怎么办？**
A：立刻去钉钉开放平台，在应用的"基础信息"页面重置 AppSecret，然后更新 OpenClaw 配置，运行 `openclaw gateway restart`。

---

## 📋 快速命令参考表

| 命令 | 作用 |
| :--- | :--- |
| `openclaw plugins install @adongguo/openclaw-dingtalk` | 安装钉钉插件 |
| `openclaw config set channels.dingtalk.appKey "xxx"` | 配置 AppKey |
| `openclaw config set channels.dingtalk.appSecret "xxx"` | 配置 AppSecret |
| `openclaw config set channels.dingtalk.enabled true` | 启用钉钉通道 |
| `openclaw gateway restart` | 重启网关 |
| `openclaw gateway status` | 查看网关状态 |
| `openclaw logs --follow` | 实时查看运行日志 |
| `openclaw pairing approve dingtalk <CODE>` | 批准配对请求 |
| `openclaw doctor` | 全面体检 |

---

## 📋 机器人聊天指令

在钉钉里直接发送以下文字给机器人：

| 指令 | 效果 |
| :--- | :--- |
| `/status` | 查看机器人状态 |
| `/new` | 清空当前会话，开始新对话 |
| `/model` | 查看或切换 AI 模型 |

---

*有问题？欢迎加入 [OpenClaw Discord 社区](https://discord.com/invite/clawd) 提问。*
