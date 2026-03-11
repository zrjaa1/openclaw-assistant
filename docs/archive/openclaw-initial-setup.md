# OpenClaw 初始化与大模型配置指南

当你成功安装 OpenClaw 后，下一步就是进行“初步部署”，也就是为你的 OpenClaw 接入一个聪明的 AI 大脑（大语言模型）。

---

## 🚀 第一步：启动配置向导
一般情况下，在OpenClaw安装成功之后会默认进入配置界面。如果没有，请打开你的命令行窗口（Windows 用户打开 PowerShell，Mac/Linux 用户打开终端），输入以下命令并按下回车：

```bash
openclaw onboard
```

*(💡 提示：如果你希望 OpenClaw 以后在电脑开机时自动在后台默默运行，可以使用 `openclaw onboard --install-daemon` 命令来代替上面的命令。)*

---

## 📋 第二步：向导选项“标准答案”对照表

程序启动后，请使用键盘 **上下方向键** 选择，按 **回车键** 确认。国内用户推荐参考下表进行配置：

| 步骤 | 你看到的选项/问题 | 推荐选择/操作 | 备注 |
| :--- | :--- | :--- | :--- |
| **1** | **I understand this is personal-by-default and shared/multi-user use requires lock-down. Continue?** | `Yes` | 确认已知晓实验性软件风险 |
| **2** | **Onboarding mode** | `QuickStart` | 快速开始模式最适合新手 |
| **3** | **Model/auth provider** | `Qwen`, `MiniMax`或者 `Moonshot AI` | **首选推荐**，国内直连且极便宜 |
| **4** | **API Key** | 粘贴你的密钥 | 粘贴时屏幕不显示字符是正常的 |
| **5** | **Select Model** | 选列表默认或者第一个 | 之后可以按需修改 |
| **6** | **Select channel (QuickStart)** | `Skip for now` | 建议先跳过，稍后再配微信/飞书 |
| **7** | **Search Provider** | `Skip for now` | 建议先跳过|
| **8** | ** Configure skills now? (recommended)** | `No` | 选 “No”（先基础运行，以后再加功能）|
| **9** | **Install Daemon** | `Yes` | 允许 OpenClaw 在后台持续运行 |

## 🛠️ 第三步：自检与故障排除

配置完成后，如果一切正常，你的 AI 助手已经准备好了。你可以运行以下命令来检查身体状况：

### 1. 自动体检 (推荐)
```bash
openclaw doctor
```
> **说明：** 这个命令会自动检查你的网络、模型连接、系统权限。如果看到满屏幕的绿色 `✓`，说明你已经完美起飞！

### 2. 启动可视化控制面板
```bash
openclaw dashboard
```
> **说明：** 这会直接在浏览器里打开一个漂亮的网页界面，你可以在那里直观地聊天或修改设置。

---

## 🔑 常用国内大模型密钥 (API Key) 获取地址

- **DeepSeek:** [platform.deepseek.com](https://platform.deepseek.com)
- **Kimi (月之暗面):** [platform.moonshot.cn](https://platform.moonshot.cn)
- **通义千问 (阿里云):** [bailian.aliyun.com](https://bailian.aliyun.com)

---

## ❓ 常见初始化问题

**Q: 粘贴 API Key 后按回车没反应？**
A: 命令行为了安全，输入密码类字符时是不显示的（连星号都没有）。只要你确定刚才粘贴了，直接按回车即可。

**Q: `openclaw doctor` 提示网络连接失败？**
A: 如果你选的是国外模型（OpenAI/Claude），请检查你的科学上网环境；如果你选的是国内模型（DeepSeek等），请检查你的 API Key 是否输入正确或已余额不足。