# OpenClaw 初始化与大模型配置指南

当你成功安装 OpenClaw 后，下一步就是为你的 AI 助手接入一个"大脑"（AI 大语言模型）。本指南帮你用**最少的步骤**完成最基本的配置，让 OpenClaw 跑起来。

> 💡 **提示：** 本指南的目标是"先跑起来"。很多可选功能（飞书接入、微信接入、技能安装等）我们都会跳过，等基础配置跑通后再慢慢加。

---

## ✅ 开始之前：确认安装成功

在开始配置之前，请先确认 OpenClaw 已经正确安装：

```bash
openclaw --version
```

如果能看到版本号（比如 `1.x.x`），说明安装成功，继续往下走。

> ⚠️ **如果提示"找不到命令"或"不是内部或外部命令"：** 说明安装还没完成或 PATH 有问题。请先回到安装指南完成安装，或者告诉我你的情况，我来帮你排查。

---

## 🚀 第一步：启动配置向导

打开你的命令行窗口（Windows 用 PowerShell，Mac/Linux 用终端），输入：

```bash
openclaw onboard
```

> 💡 **提示：** 如果你希望 OpenClaw 以后在电脑开机时自动在后台运行，可以用 `openclaw onboard --install-daemon` 来代替上面的命令。推荐使用这个。

---

## 📋 第二步：按照向导提示选择配置

程序启动后，请使用键盘**上下方向键**选择，按**回车键**确认。以下是每一步的推荐选择：

### 选项 1：安全确认
> **I understand this is personal-by-default and shared/multi-user use requires lock-down. Continue?**

选 **Yes** — 这只是告诉你 OpenClaw 默认是个人使用模式，确认即可。

### 选项 2：配置模式
> **Onboarding mode**

选 **QuickStart** — 快速模式，会跳过很多高级选项，最适合新手。

### 选项 3：AI 模型提供商（最重要的一步）
> **Model/auth provider**

这一步是选择你的 AI 助手使用哪个"大脑"。

**国内用户推荐（直连，无需科学上网）：**

| 模型提供商 | 特点 | 推荐程度 |
| :--- | :--- | :--- |
| **Qwen（通义千问）** | 阿里云出品，中文能力强 | ⭐⭐⭐ 首选推荐 |
| **MiniMax** | 国产模型，速度快 | ⭐⭐ |
| **Moonshot AI（Kimi）** | 月之暗面，擅长长文本 | ⭐⭐ |
| **DeepSeek** | 性价比极高 | ⭐⭐ |

**有科学上网的用户也可以选：**

| 模型提供商 | 特点 | 注意事项 |
| :--- | :--- | :--- |
| **OpenAI (GPT)** | 全球最知名 | 需要科学上网 + 海外手机号注册 |
| **Anthropic (Claude)** | 推理能力强 | 需要科学上网 |
| **Google (Gemini)** | 多模态能力好 | 需要科学上网 |

> 💡 **提示：** 如果不确定选哪个，**选 Qwen** 就对了。国内直连、速度快、中文好、价格便宜。

### 选项 4：填入 API Key
> **API Key**

这里需要粘贴你的 API 密钥。API Key 是你在 AI 模型提供商那里申请的一个"通行证"。

**还没有 API Key？** 以下是常用模型的申请地址：

| 模型 | 申请地址 | 说明 |
| :--- | :--- | :--- |
| **通义千问 (Qwen)** | [bailian.aliyun.com](https://bailian.aliyun.com) | 阿里云百炼平台，新用户有免费额度 |
| **DeepSeek** | [platform.deepseek.com](https://platform.deepseek.com) | 注册后直接获取 Key |
| **Kimi (月之暗面)** | [platform.moonshot.cn](https://platform.moonshot.cn) | 注册后创建 Key |
| **MiniMax** | [platform.minimaxi.com](https://platform.minimaxi.com) | 注册后获取 Key |

> ⚠️ **注意：** 粘贴 API Key 时，屏幕上**不会显示任何字符**（连星号都没有），这是命令行的安全设计，不是出了问题。你只管粘贴，然后按回车。

### 选项 5：选择具体模型
> **Select Model**

选列表中的**默认选项或第一个**即可。以后随时可以通过 `/model` 命令切换。

### 选项 6：通讯渠道
> **Select channel (QuickStart)**

选 **Skip for now** — 飞书、微信等渠道的接入比较复杂，我们以后单独配置。现在先跳过。

### 选项 7：搜索引擎
> **Search Provider**

选 **Skip for now** — 搜索功能是可选的，以后需要再配。

### 选项 8：技能（Skills）
> **Configure skills now?**

选 **No** — 技能也是可选的增强功能，基础运行不需要。

### 选项 9：后台服务
> **Install Daemon**

选 **Yes** — 这样 OpenClaw 会在后台持续运行，关掉命令行窗口也不会断。

---

### ❓ 配置向导常见问题

**Q：粘贴 API Key 后按回车没反应？**
A：命令行出于安全考虑，输入密码类内容时不显示任何字符（连星号都没有）。这是正常行为，只要你确实粘贴了内容，直接按回车即可。

**Q：选错了模型怎么办？**
A：不用担心，以后随时可以通过 `openclaw onboard` 重新运行向导来修改，或者直接编辑配置文件。

**Q：API Key 从哪里获取？需要花钱吗？**
A：各平台都需要注册账号后才能获取 API Key。大部分国内平台（通义千问、DeepSeek 等）注册后都有**免费额度**，足够你体验和日常使用。用完后需要充值，但价格通常很便宜（几元到几十元就能用很久）。

**Q：向导中途退出了怎么办？**
A：重新运行 `openclaw onboard` 即可，不会影响已有配置。

---

## 🔒 第三步：设置安全权限（重要！）

配置向导完成后，强烈建议你在正式使用之前先设置一个合适的权限级别。

从 2026.3.2 版本开始，新安装的小龙虾默认使用「安全模式」，只能收发消息。这已经是一个安全的起点。如果你是老版本升级过来的用户，你的小龙虾可能仍在使用「完全权限」模式，建议调整。

**我们提供 4 个权限级别：**

**1. 安全模式（Safe Mode）— 默认，新手推荐**

只能收发消息，不能读写文件或执行命令。新安装（2026.3.2+）的默认设置。如果你是新安装的用户，不需要做任何设置。

**2. 只读模式（Read-Only Mode）**

在安全模式基础上，还可以阅读本地文件、浏览网页、分析图片和 PDF、读取记忆。但不能创建或修改文件。注意：不能保存新的记忆。

请根据你的操作系统选择对应的命令：

macOS / Linux（bash/zsh）：
```bash
openclaw config set tools.deny '["write","edit","apply_patch","exec","process","sessions_spawn","nodes","canvas","cron","gateway"]'
```

Windows（PowerShell）：
```powershell
openclaw config set tools.deny '[\"write\",\"edit\",\"apply_patch\",\"exec\",\"process\",\"sessions_spawn\",\"nodes\",\"canvas\",\"cron\",\"gateway\"]'
```

**3. 读写模式（Read & Write Mode）— 进阶推荐**

在只读模式基础上，还可以创建和修改文件、保存长期记忆。但不能执行终端命令。

macOS / Linux（bash/zsh）：
```bash
openclaw config set tools.deny '["exec","process","sessions_spawn","nodes","canvas","cron","gateway"]'
```

Windows（PowerShell）：
```powershell
openclaw config set tools.deny '[\"exec\",\"process\",\"sessions_spawn\",\"nodes\",\"canvas\",\"cron\",\"gateway\"]'
```

**4. 完全权限（Full Mode）— 高级用户，慎用**

没有任何限制。可以执行命令、控制浏览器、管理设备等。老版本（2026.3.2 之前）的默认设置。⚠️ 除非你完全了解这些权限的含义，否则不建议使用。

```
openclaw config set tools.deny '[]'
```

**设置完后，重启小龙虾让设置生效：**

```
openclaw gateway restart
```

> 💡 **提示：** 新安装用户已经是安全模式，可以跳过这步。需要更多功能时，随时可以运行上面的命令升级。

---

## 🛠️ 第四步：自检与确认

配置完成后，运行以下命令做一次全面体检：

```bash
openclaw doctor
```

**看到什么说明成功了？**
- 所有检查项都显示绿色 `✓` → 完美，一切就绪！🎉
- 大部分绿色，只有个别黄色 `⚠` → 基本没问题，黄色通常是可选功能未配置
- 出现红色 `✗` → 有问题需要解决，请把错误信息告诉我

---

### ❓ 自检常见问题

**Q：`openclaw doctor` 提示网络连接失败？**
A：
- 如果你选的是**国内模型**（Qwen、DeepSeek 等）：请检查 API Key 是否正确，以及账户余额是否充足
- 如果你选的是**国外模型**（OpenAI、Claude 等）：请检查科学上网是否正常工作，终端是否也走了代理

**Q：提示模型连接超时？**
A：可能是网络不稳定。等几分钟后再运行一次 `openclaw doctor`。如果反复超时，可以考虑换一个模型提供商。

---

## 🎉 第五步：开始使用

恭喜！基础配置已经完成。以下是开始使用的最快方式：

### 打开控制面板（推荐新手）

```bash
openclaw dashboard
```

这会在浏览器里打开一个网页界面，你可以直接在上面和 AI 助手聊天。

### 或者直接在命令行聊天

```bash
openclaw
```

---

## 📋 常用命令速查

| 命令 | 作用 |
| :--- | :--- |
| `openclaw onboard` | 重新运行配置向导（修改模型、Key 等） |
| `openclaw dashboard` | 打开浏览器控制面板 |
| `openclaw doctor` | 自动体检（检查配置和连接） |
| `openclaw gateway start` | 启动后台服务 |
| `openclaw gateway stop` | 停止后台服务 |
| `openclaw gateway status` | 查看后台服务状态 |
| `openclaw status` | 查看当前配置状态 |

---

## ❓ 综合常见问题

**Q：配置好了，下一步可以做什么？**
A：基础版已经可以通过 `openclaw dashboard` 和 AI 聊天了。如果你想让 AI 助手接入飞书或微信，我可以指导你配置。

**Q：想换一个 AI 模型怎么办？**
A：重新运行 `openclaw onboard`，在选择模型那一步选一个新的即可。旧配置不会丢失。

**Q：API 额度用完了会怎样？**
A：AI 助手会停止回复，你会看到类似"余额不足"的错误提示。去对应平台充值即可恢复。

**Q：可以同时配置多个 AI 模型吗？**
A：可以的，但这是进阶操作。建议先用一个模型跑起来，后续我可以帮你配置多模型切换。

---

*有问题？随时告诉我你在哪一步卡住了，我来帮你。*
