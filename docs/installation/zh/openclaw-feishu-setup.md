# 飞书（Feishu）接入配置指南

本指南将带你一步步完成 OpenClaw 与飞书（Feishu）的连接配置，让你的 AI 助手住进飞书，随时响应你的消息。

> 💡 **提示：** 如果你使用的是 **Lark（飞书国际版）**，操作步骤完全相同，但需要访问 [open.larksuite.com](https://open.larksuite.com/app)，并在最后的配置文件里额外加一行 `domain: "lark"`，本文末尾会专门说明。

---

## ✅ 前置条件（开始之前请确认）

在配置飞书之前，请先确认以下几项都已完成：

- ✅ **OpenClaw 已安装** — 在终端输入 `openclaw --version`，能看到版本号说明安装成功
- ✅ **大模型已配置** — 运行 `openclaw doctor`，结果全绿（没有红色 ✗）
- ✅ **网关可以正常启动** — 运行 `openclaw gateway`，没有报错

> 💡 **提示：** 如果以上任何一项不满足，说明基础配置还没完成。请先运行 `openclaw onboard` 完成初始化配置（选择一个大模型、填入 API Key），确认 `openclaw doctor` 全绿后再回来继续。

> ⚠️ **不确定怎么做？** 直接告诉我你的情况（比如"我还没装 OpenClaw"或"openclaw doctor 有红色的"），我会先帮你搞定基础配置。

---

## 🚀 第一步：安装飞书插件

在开始一切之前，先确保 OpenClaw 已经安装了飞书插件。打开你的命令行窗口（Windows 用户打开 PowerShell，Mac/Linux 用户打开终端），输入：

```bash
openclaw plugins install @openclaw/feishu
```

---

## 📋 第二步：创建飞书应用

飞书机器人需要通过"企业自建应用"的方式接入。别担心，这不需要任何代码，就像注册一个账号一样简单。

### 操作步骤

**步骤 1：** 打开浏览器，访问飞书开放平台：[https://open.feishu.cn/app](https://open.feishu.cn/app)

用你的飞书账号登录。

> ⚠️ **注意：** 你需要有企业管理员权限，或者向管理员申请"开发者"权限，才能创建自建应用。

**步骤 2：** 点击页面上的 **"创建企业自建应用"** 按钮。

**步骤 3：** 填写应用信息：
- **应用名称**：随便起，比如 "我的 AI 助手"
- **应用描述**：可以写 "OpenClaw AI 机器人"
- **应用图标**：可以上传一张你喜欢的图片，也可以先跳过

**步骤 4：** 点击 **"确认创建"**，应用就建好了！

**步骤 5：** 进入应用后，找到左侧菜单中的 **"凭证与基础信息"**（Credentials & Basic Info），你会看到两个重要的东西：

- **App ID**：格式类似 `cli_xxxxxxxxxxxxxxxx`
- **App Secret**：一串看起来像乱码的字符

> ⚠️ **注意：** `App Secret` 是你的应用密钥，相当于密码，**绝对不要分享给任何人**。如果不小心泄露了，请立刻在同一页面点击"重置"。

**步骤 6：** 把 **App ID** 和 **App Secret** 都复制下来，找个地方暂时保存（比如记事本），后面要用。

---

### ❓ 常见问题

**Q：我找不到"创建企业自建应用"按钮？**
A：可能你的账号没有开发者权限。请联系你的飞书企业管理员，让他们在"飞书管理后台 → 工作台 → 应用管理 → 企业自建应用"里给你开权限，或者让管理员帮你创建应用。

**Q：App ID 和 App Secret 在哪里？**
A：进入你的应用，左侧菜单点 **"凭证与基础信息"**，就在页面中间位置。

---

## 📋 第三步：配置应用权限

机器人需要一些"读写消息"的权限才能正常工作。飞书提供了批量导入功能，我们直接用 JSON 一键搞定，不需要一个一个手动勾选。

### 操作步骤

**步骤 1：** 在应用左侧菜单，点击 **"权限管理"**（Permissions）。

**步骤 2：** 点击页面里的 **"批量添加"** 或 **"批量导入"** 按钮（具体名称依飞书版本而定）。

**步骤 3：** 将以下 JSON 内容**完整复制**，粘贴进去，然后点击确认：

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "cardkit:card:read",
      "cardkit:card:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "event:ip_list",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": ["aily:file:read", "aily:file:write", "im:chat.access_event.bot_p2p_chat:read"]
  }
}
```

**步骤 4：** 确认后，你应该能看到列表里出现了一批权限条目。

> 💡 **提示：** 这些权限涉及"发送消息"、"读取消息"、"管理机器人菜单"等功能。如果你的企业安全政策比较严格，管理员可能需要审批这些权限。

---

### ❓ 常见问题

**Q：找不到"批量导入"按钮怎么办？**
A：不同版本的飞书开放平台界面可能略有差异。你可以在"权限管理"页面搜索关键词（比如 `im:message`）来手动添加，也可以点击"添加权限"后一条一条查找。核心必须有的权限是 `im:message:send_as_bot`（发消息）和 `im:message.p2p_msg:readonly`（收私信）。

**Q：权限被标为"需要审批"是什么意思？**
A：部分权限需要企业管理员审批才能生效。你需要联系你的飞书管理员，让他们在"飞书管理后台"里批准你的应用权限申请。审批通过后，权限才会真正生效。

---

## 📋 第四步：开启机器人能力

现在来"告诉"飞书，这个应用要作为一个机器人运作。

### 操作步骤

**步骤 1：** 在应用左侧菜单，找到 **"应用能力"**（App Capability）或 **"添加应用能力"**，点击进入。

**步骤 2：** 找到 **"机器人"**（Bot）这一项，点击 **"开启"** 或 **"添加"**。

**步骤 3：** 开启后，你可以设置机器人的名字（就是它在飞书聊天里显示的名字）。

**步骤 4：** 点击 **"保存"** 或 **"确认"**。

> 💡 **提示：** 机器人名字可以和应用名字不同，比如应用叫"我的 AI 助手"，机器人昵称可以叫"小智"。用户在聊天里看到的是机器人昵称。

---

### ❓ 常见问题

**Q：没有找到"机器人"这个能力选项？**
A：部分老版本的应用可能显示方式不同。请在"应用能力"页面往下滚，或者尝试点击"开通能力"按钮，在弹出的列表里找"机器人"。

---

## 📋 第五步：配置事件订阅

这一步让飞书知道"有人给机器人发消息了，请通知 OpenClaw"。这里使用**长连接模式**（WebSocket），不需要公网服务器，普通家庭网络也能用。

> ⚠️ **重要提醒：** 在做这一步之前，你需要先完成**第六步（配置 OpenClaw）**，并且让 **OpenClaw 网关保持运行状态**。否则长连接可能无法保存成功。

**建议的操作顺序：**
1. 先跳到 [第六步：配置 OpenClaw](#第六步配置-openclaw) 完成配置
2. 启动网关：`openclaw gateway`
3. 回来完成本步骤

---

如果你已经完成了第六步并启动了网关，继续：

### 操作步骤

**步骤 1：** 在应用左侧菜单，点击 **"事件与回调"**（Event Subscription）或 **"事件订阅"**。

**步骤 2：** 在"订阅方式"中，选择 **"使用长连接接收事件"**（Use long connection to receive events）。

> 💡 **提示：** 选"长连接"而不是"将事件发送到开发者服务器"，是因为长连接不需要你有公网 IP 或服务器，OpenClaw 会主动连接飞书，而不是等飞书来找你。

**步骤 3：** 点击 **"添加事件"** 按钮，在搜索框里输入 `im.message.receive_v1`，找到后点击添加。

**步骤 4：** 点击 **"保存"** 或 **"确认"**。

> ⚠️ **注意：** 如果保存时提示错误，请先确认 OpenClaw 网关正在运行（`openclaw gateway status` 看到 `running` 才算）。

---

### ❓ 常见问题

**Q：添加事件后提示"连接失败"或无法保存？**
A：十有八九是网关没启动。回到终端，先运行 `openclaw gateway`，等看到网关启动成功的提示后，再回来保存事件订阅。

**Q：我找不到 `im.message.receive_v1` 这个事件？**
A：在搜索框里输入 `im.message.receive`，应该能看到它出现在列表里。如果还找不到，确认你的应用已经开启了"机器人能力"（第四步）。

---

## 📋 第六步：发布应用

应用创建好后需要"发布"才能正式使用，就像 App 上架应用商店一样。

### 操作步骤

**步骤 1：** 在应用左侧菜单，点击 **"版本管理与发布"**（Version Management & Release）。

**步骤 2：** 点击 **"创建版本"**（Create Version）。

**步骤 3：** 填写版本信息：
- **版本号**：比如 `1.0.0`
- **更新说明**：随便写，比如 "初始版本"

**步骤 4：** 点击 **"保存"**，然后点击 **"申请发布"** 或 **"提交审核"**。

**步骤 5：** 等待审核通过。

> 💡 **提示：** 大多数企业自建应用**无需外部审核**，提交后管理员在飞书管理后台"工作台 → 应用审核"里一键通过即可，通常几分钟内搞定。如果超过一天没通过，请联系你的飞书管理员。

---

### ❓ 常见问题

**Q：找不到"版本管理与发布"菜单？**
A：不同版本的飞书开放平台界面可能不同。可以尝试找"发布"或"上线"字样的菜单项，也可以在应用首页查看是否有"发布"按钮。

**Q：审核一直是"审核中"没有通过？**
A：企业自建应用审核完全在你自己公司内部，需要你们飞书的管理员操作。如果等了很久，请直接联系管理员，让他在"飞书管理后台 → 工作台 → 待审核应用"里找到你的应用并通过。

---

## 🛠️ 第七步：配置 OpenClaw

现在把刚才拿到的 App ID 和 App Secret 填进 OpenClaw 里。

### 方式一：使用配置向导（推荐新手）

这是最简单的方式，向导会一步步问你问题：

```bash
openclaw channels add
```

程序启动后：

1. 用方向键找到 **"Feishu"**，按回车确认
2. 在 **"App ID"** 提示处，粘贴你的 App ID（格式 `cli_xxx`）
3. 在 **"App Secret"** 提示处，粘贴你的 App Secret

向导完成后，配置会自动保存。

---

### 方式二：直接编辑配置文件（适合熟悉配置文件的用户）

配置文件位于 `~/.openclaw/openclaw.json`。用文本编辑器打开，添加或修改 `channels.feishu` 部分：

```json5
{
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "pairing",
      "accounts": {
        "main": {
          "appId": "cli_xxx",
          "appSecret": "在这里填你的App Secret",
          "botName": "我的AI助手"
        }
      }
    }
  }
}
```

> ⚠️ **注意：** `appId` 和 `appSecret` 都要换成你自己的值，不要照抄示例里的 `cli_xxx`。

两种配置方式的对比：

| 特性 | 配置向导 | 编辑配置文件 |
| :--- | :--- | :--- |
| **难度** | ⭐ 简单，有提示 | ⭐⭐ 需要了解 JSON 格式 |
| **适合人群** | 新手、非技术用户 | 技术用户、需要高级配置 |
| **高级选项** | 基础选项 | 支持所有高级配置 |
| **出错风险** | 低 | JSON 格式写错会报错 |

> 💡 **提示：** 如果你不确定该用哪种方式，就用向导（方式一）。配置完成后随时可以用文本编辑器打开配置文件查看或修改。

---

### Lark 国际版用户额外步骤

如果你用的是 **Lark（飞书国际版，域名为 larksuite.com）**，需要在配置文件里加一行 `domain: "lark"`：

```json5
{
  "channels": {
    "feishu": {
      "domain": "lark",
      "accounts": {
        "main": {
          "appId": "cli_xxx",
          "appSecret": "你的App Secret"
        }
      }
    }
  }
}
```

---

### ❓ 常见问题

**Q：`~/.openclaw/openclaw.json` 文件找不到？**
A：这个文件在你的用户主目录下的 `.openclaw` 文件夹里。
- Mac/Linux：打开 Finder 或文件管理器，按 `Cmd+Shift+G`（Mac）输入 `~/.openclaw`；或在终端输入 `open ~/.openclaw`
- Windows：在文件资源管理器地址栏输入 `%USERPROFILE%\.openclaw`

**Q：配置文件里已经有其他内容了，我直接加 feishu 部分会不会破坏原来的配置？**
A：只要 JSON 格式正确就没问题。把 `"feishu": { ... }` 作为 `"channels"` 对象里的一个新键值对加进去就行。如果不确定格式，建议用向导方式（方式一）。

---

## 🛠️ 第八步：启动并测试

配置完成，现在来让机器人跑起来！

### 操作步骤

**步骤 1：** 启动 OpenClaw 网关：

```bash
openclaw gateway
```

> 💡 **提示：** 网关是 OpenClaw 的"后台服务"，它负责和飞书保持连接。只要网关在运行，机器人就在线。

**步骤 2：** 确认网关状态：

```bash
openclaw gateway status
```

看到输出中包含 `running` 字样就说明正常运行了。

**步骤 3：** 打开飞书，在"搜索"里找到你刚创建的机器人（用应用名字或机器人名字搜索），点开对话框。

**步骤 4：** 发一条消息，比如"你好"。

**步骤 5：** 机器人会回复一个**配对码**（pairing code），格式类似：`PAIR-XXXXXX`。这是安全验证步骤，防止陌生人连接。

**步骤 6：** 回到你的终端，输入以下命令来批准这个配对请求（把 `XXXXXX` 换成你收到的实际配对码）：

```bash
openclaw pairing approve feishu XXXXXX
```

**步骤 7：** 批准后，再在飞书里发一条消息，机器人就会正常回复你了！🎉

**步骤 8：** 最后，运行一次全面体检，确认飞书连接一切正常：

```bash
openclaw doctor
```

看到飞书相关的检查项全部显示绿色 `✓` 就说明配置完美！如果有红色 `✗`，根据提示信息排查（通常是权限或网关问题）。

---

### 查看实时日志

如果机器人没有反应，可以用以下命令查看实时日志排查问题：

```bash
openclaw logs --follow
```

按 `Ctrl+C` 退出日志查看。

---

### ❓ 常见问题

**Q：发消息后机器人没有任何反应？**
A：按顺序检查：
1. `openclaw gateway status` — 网关是否运行中（看到 `running`）？
2. `openclaw logs --follow` — 日志里有没有报错？
3. 应用是否已发布并通过审核？（第六步）
4. 事件订阅是否已保存？（第五步）
5. 权限是否都已批准？（第三步）

**Q：机器人回复了配对码，但我输入 `openclaw pairing approve` 后说找不到这个码？**
A：配对码有时效，如果超过几分钟没有批准可能会过期。在飞书里再发一条消息，会重新收到配对码，然后立刻去批准。

**Q：我不想每次都手动批准，能不能让所有人自动连上？**
A：可以把 `dmPolicy` 改为 `"open"` 并在 `allowFrom` 里加 `"*"`，这样所有人发消息都不需要配对。但这意味着任何知道你机器人名字的人都能使用它，不建议在生产环境这样设置。更安全的做法是把允许的用户 ID 加到 `allowFrom` 列表里。

---

## 📋 第九步：群聊配置（可选）

如果你想让机器人在飞书群聊里也能使用，需要做一点额外配置。

### 把机器人添加到群聊

**步骤 1：** 打开你想添加机器人的飞书群聊。

**步骤 2：** 点击右上角的"群设置"图标（通常是一个齿轮或者"..."）。

**步骤 3：** 找到 **"群机器人"** 或 **"添加机器人"** 选项，点击添加。

**步骤 4：** 在列表里找到你的应用/机器人，添加进来。

---

### 群聊 @mention 行为

机器人在群聊里默认**只响应 @它 的消息**，这样它不会在每条群消息都插嘴。

| 配置 | 效果 |
| :--- | :--- |
| 默认（`requireMention: true`） | 必须 @机器人 才会回复 |
| `requireMention: false` | 群里所有消息都会触发机器人 |

如果你想让某个特定群不需要 @mention 就能触发机器人，在配置文件里这样设置：

```json5
{
  "channels": {
    "feishu": {
      "groups": {
        "oc_xxx": {
          "requireMention": false
        }
      }
    }
  }
}
```

> 💡 **提示：** `oc_xxx` 是群的 ID（chat_id）。如何找到群 ID？启动网关后，在群里 @一次机器人，然后运行 `openclaw logs --follow`，在日志里找 `chat_id` 字段，它的值就是群 ID。

---

### 群聊访问控制

如果你想控制哪些群可以使用机器人，可以设置群聊策略：

| 策略 | 配置值 | 效果 |
| :--- | :--- | :--- |
| 所有群都可以用（默认） | `groupPolicy: "open"` | 添加了机器人的群都可以使用 |
| 只允许指定群 | `groupPolicy: "allowlist"` | 只有 `groupAllowFrom` 列表里的群才能用 |
| 完全禁用群聊 | `groupPolicy: "disabled"` | 机器人在所有群都不响应 |

---

### ❓ 常见问题

**Q：机器人加到群里了，@它 也没反应？**
A：
1. 确认机器人已经成功加入群聊（群设置里能看到它）
2. 确认 `groupPolicy` 不是 `"disabled"`
3. @mention 时要用飞书的 @功能（输入 `@` 然后从下拉菜单选择机器人），不是手动打机器人名字
4. 运行 `openclaw logs --follow` 查看日志，看是否有消息进来

**Q：如何只允许群里特定的人使用机器人？**
A：可以在配置里给具体的群设置 `allowFrom` 用户列表：
```json5
{
  "channels": {
    "feishu": {
      "groups": {
        "oc_xxx": {
          "allowFrom": ["ou_用户1的ID", "ou_用户2的ID"]
        }
      }
    }
  }
}
```
只有列表里的用户发的消息（即使 @了机器人）才会被处理。用户 ID（`ou_xxx`）可以通过 `openclaw pairing list feishu` 或者查看日志获取。

---

## ❓ 综合常见问题

**Q：应用一切正常，但有时候消息会有延迟？**
A：飞书长连接偶尔会断开并自动重连，短暂延迟（几秒内）是正常的。如果延迟超过一分钟，运行 `openclaw gateway restart` 重启网关试试。

**Q：我的 App Secret 泄露了怎么办？**
A：立刻去飞书开放平台，进入你的应用，在"凭证与基础信息"页面点击 **重置 App Secret**，然后把新的 App Secret 更新到 OpenClaw 配置文件里，再运行 `openclaw gateway restart`。

**Q：我想让机器人 24 小时运行，不能一直开着终端怎么办？**
A：可以把 OpenClaw 安装为系统服务，这样关掉终端也会在后台运行：
```bash
openclaw gateway install
```
安装后用 `openclaw gateway status` 确认状态，用 `openclaw gateway stop` 停止服务。

**Q：飞书版本更新后，机器人突然不工作了？**
A：先检查应用的权限和发布状态是否有变化（飞书有时会在版本更新后要求重新发布应用）。再运行 `openclaw gateway restart`，然后 `openclaw logs --follow` 查看具体报错信息。

**Q：可以在同一个 OpenClaw 上连接多个飞书账号/应用吗？**
A：可以！在配置文件的 `accounts` 里添加多个账号即可：
```json5
{
  "channels": {
    "feishu": {
      "defaultAccount": "main",
      "accounts": {
        "main": {
          "appId": "cli_xxx",
          "appSecret": "xxx",
          "botName": "主机器人"
        },
        "second": {
          "appId": "cli_yyy",
          "appSecret": "yyy",
          "botName": "备用机器人"
        }
      }
    }
  }
}
```

**Q：这份指南里的截图在哪里？**
A：飞书开放平台的界面会随版本更新而变化，所以本指南以文字描述为主，确保长期有效。如果你实在找不到某个菜单，可以在飞书开放平台的帮助文档里搜索，或者在 [OpenClaw 社区](https://discord.com/invite/clawd) 提问。

---

## 📋 快速命令参考表

| 命令 | 作用 |
| :--- | :--- |
| `openclaw plugins install @openclaw/feishu` | 安装飞书插件 |
| `openclaw channels add` | 添加飞书频道（配置向导） |
| `openclaw gateway` | 启动网关 |
| `openclaw gateway status` | 查看网关状态 |
| `openclaw gateway install` | 安装为系统后台服务 |
| `openclaw gateway restart` | 重启网关 |
| `openclaw gateway stop` | 停止网关 |
| `openclaw logs --follow` | 实时查看运行日志 |
| `openclaw pairing list feishu` | 查看等待配对的请求 |
| `openclaw pairing approve feishu <CODE>` | 批准配对请求 |

---

## 📋 机器人聊天指令

在飞书里直接发送以下文字给机器人即可触发指令：

| 指令 | 效果 |
| :--- | :--- |
| `/status` | 查看机器人当前状态 |
| `/reset` | 清空当前会话，重新开始 |
| `/model` | 查看或切换当前使用的 AI 模型 |

> 💡 **提示：** 飞书目前不支持原生命令菜单，所以这些指令需要直接在聊天框里输入发送。

---

*有问题？欢迎加入 [OpenClaw Discord 社区](https://discord.com/invite/clawd) 提问。*
