# OpenClaw 常见问题总览 (FAQ)

本文档汇总了安装和初始配置过程中最常见的问题及解决方案。如果你在任何步骤遇到问题，先来这里找找答案。

---

## 🔧 安装相关

### Q：运行安装命令后提示"无法加载脚本"或"执行策略"（Windows）
A：这是 Windows 默认的安全限制。解决方法：
1. 右键点击 PowerShell → **以管理员身份运行**
2. 运行以下命令（遇到提示输入 Y 回车）：
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. 关闭管理员窗口，重新打开普通 PowerShell 继续安装

### Q：安装过程中卡住不动，进度条不走了
A：通常是网络问题。
1. 按 `Ctrl + C` 终止当前操作
2. 检查网络连接
3. 如果在中国大陆，尝试使用国内镜像安装：
   ```bash
   npm install -g openclaw-cn@latest --registry=https://registry.npmmirror.com
   ```

### Q：提示 Node.js 版本不对或未安装
A：OpenClaw 需要 Node.js 22 或更高版本。
- 检查版本：`node -v`
- 如果低于 22 或未安装，前往 [nodejs.org/zh-cn](https://nodejs.org/zh-cn) 下载最新 LTS 版本安装
- 安装后**必须关闭终端重新打开**

### Q：`openclaw` 命令找不到（"不是内部或外部命令"）
A：PATH 环境变量没有正确配置。
1. 运行 `npm prefix -g` 查看 npm 全局路径
2. 把这个路径加到系统 PATH 中：
   - **Windows：** 设置 → 搜索"环境变量" → 编辑 Path → 添加上面的路径
   - **Mac/Linux：** 运行 `echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc`
3. 关闭终端，重新打开

### Q：提示 "npm error spawn git ENOENT"
A：需要安装 Git。
- Windows：下载安装 [git-scm.com/downloads/win](https://git-scm.com/downloads/win)
- Mac：终端运行 `xcode-select --install`
- 安装后关闭终端重新打开

### Q：Mac 弹出"需要安装命令行开发者工具"
A：点击 **"安装"** 按钮，等待完成后重新运行安装命令。这是正常的。

### Q：Linux 上 `npm install -g` 提示权限不足 (EACCES)
A：运行以下命令修复：
```bash
mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
然后重新安装。

### Q：我的电脑是 Windows 7 / 32 位系统，能安装吗？
A：很遗憾不行。OpenClaw 需要 Windows 10 或更高版本的 64 位系统。建议升级操作系统后再尝试。

---

## ⚙️ 初始配置相关

### Q：粘贴 API Key 后按回车，屏幕上什么都没显示
A：这是正常的安全设计。命令行在输入密码类内容时不会显示任何字符（连星号都没有）。只要你确实粘贴了内容，直接按回车即可。

### Q：API Key 从哪里获取？需要花钱吗？
A：在你选择的 AI 模型提供商平台注册后获取。常用平台：
- **通义千问 (Qwen)：** [bailian.aliyun.com](https://bailian.aliyun.com) — 有免费额度
- **DeepSeek：** [platform.deepseek.com](https://platform.deepseek.com) — 有免费额度
- **Kimi：** [platform.moonshot.cn](https://platform.moonshot.cn) — 有免费额度

大部分平台注册后都有免费额度，日常使用费用通常很低（几元到几十元）。

### Q：`openclaw doctor` 提示网络连接失败
A：
- 国内模型（Qwen、DeepSeek 等）：检查 API Key 是否正确、账户是否有余额
- 国外模型（OpenAI、Claude 等）：检查科学上网是否正常，终端是否也走了代理

### Q：选错了模型怎么办？
A：重新运行 `openclaw onboard` 即可修改。不会影响已有的其他配置。

### Q：配置文件在哪里？
A：`~/.openclaw/openclaw.json`
- **Mac/Linux：** 终端运行 `open ~/.openclaw`（Mac）或 `xdg-open ~/.openclaw`（Linux）
- **Windows：** 文件资源管理器地址栏输入 `%USERPROFILE%\.openclaw`

### Q：修改了配置文件，怎么让它生效？
A：运行 `openclaw gateway restart` 重启网关。

### Q：JSON 配置文件格式写错了
A：OpenClaw 会在启动时报错并告诉你哪里有问题。常见错误：
- 缺少逗号或多了逗号
- 引号不匹配
- 大括号/方括号不匹配

可以用在线工具（如 [jsonlint.com](https://jsonlint.com)）检查格式。

---

## 🌐 网关和连接相关

### Q：网关启动失败
A：
1. 运行 `openclaw logs --follow` 查看具体错误
2. 常见原因：端口被占用、配置文件格式错误、API Key 无效
3. 尝试 `openclaw gateway restart`

### Q：网关在运行，但机器人不回复消息
A：按顺序排查：
1. 通讯平台（飞书/钉钉/微信）的应用是否已发布？
2. 事件订阅是否已正确配置？
3. 凭证（AppKey/AppSecret/API Key）是否正确？
4. 运行 `openclaw logs --follow` 查看是否收到了消息

### Q：怎么让 OpenClaw 开机自动运行？
A：运行 `openclaw gateway install`，OpenClaw 会安装为系统后台服务。
- 查看状态：`openclaw gateway status`
- 停止服务：`openclaw gateway stop`
- 启动服务：`openclaw gateway start`

### Q：配对码（pairing code）过期了
A：在通讯平台里重新给机器人发一条消息，会收到新的配对码。立刻在终端运行 `openclaw pairing approve <平台> <新配对码>`。

---

## 💡 使用相关

### Q：AI 回复很慢
A：
- 检查网络连接
- 有些模型（特别是大参数模型）确实回复较慢，可以尝试切换到更快的模型
- 运行 `openclaw doctor` 检查连接状态

### Q：API 额度用完了会怎样？
A：AI 会停止回复。去对应模型提供商平台充值即可恢复。

### Q：怎么查看当前用的是什么模型？
A：在聊天中发送 `/model` 命令即可查看和切换。

### Q：怎么清除聊天记录重新开始？
A：发送 `/reset` 命令可以清空当前会话。

---

## 🔄 更新相关

### Q：怎么更新 OpenClaw 到最新版本？
A：根据你的安装方式：
- 官方安装：重新运行安装脚本即可（会自动覆盖更新）
- npm 安装：`npm update -g openclaw`
- 国内镜像：`npm update -g openclaw-cn --registry=https://registry.npmmirror.com`

更新后运行 `openclaw doctor` 确认一切正常。

### Q：更新后原来的配置会丢失吗？
A：不会。配置文件保存在 `~/.openclaw/` 目录下，更新只会替换程序本身，不影响配置。

---

## 🆘 求助

**如果以上都没有解决你的问题：**

1. 运行以下命令，把输出结果复制给我：
   ```bash
   openclaw --version
   node -v
   openclaw doctor
   ```
2. 描述你遇到的问题和你做了什么操作
3. 如果有错误信息，请完整复制

也欢迎加入 [OpenClaw Discord 社区](https://discord.com/invite/clawd) 提问，或查阅官方文档 [docs.openclaw.ai](https://docs.openclaw.ai/zh-CN/start/getting-started)。
