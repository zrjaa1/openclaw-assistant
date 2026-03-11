# OpenClaw Windows 极简安装指南

本文档专门指导没有技术背景的 Windows 用户，在国内网络环境下顺利安装 OpenClaw。

---

## 💻 电脑配置要求

- **操作系统:** Windows 10 或 Windows 11 (64位)

---

## 🚀 方法一：官方一键安装脚本（推荐首选）

这是最自动化的安装方式，脚本会尝试帮你配置所需环境。

### 步骤 1: 打开 PowerShell
1. 按住键盘上的 `Win` 键不放，然后按 `X` 键。
2. 在弹出的菜单中，点击 **Windows PowerShell** 或 **终端**。
3. 此时屏幕上会出现一个命令行窗口。

### 步骤 2: 运行安装命令
复制下方这行代码，在刚才打开的窗口中右键粘贴，然后按下**回车键**：

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

脚本会自动尝试为你安装 Node.js 22 和 OpenClaw。 如果运行后提示“找不到 Node”或安装失败，请改用下方的【方法二】进行手动安装。

如果因为网络问题报错，请尝试使用备用 CMD 命令：
1. 按 `Win + R`，输入 `cmd`，按回车。
2. 粘贴以下命令并按回车：
```cmd
curl -fsSL https://openclaw.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

---

## 🛡️ 方法二：国内网络优化版 (openclaw-cn)

如果方法一因为网络墙的原因卡死或失败，请使用此兜底方案。本方法全部从国内淘宝镜像极速下载，成功率最高。

### 步骤 1: 手动安装前置环境（必须执行）
由于国内优化版需要依赖 npm 工具，你必须先安装 Node.js 和 Git：
1. **安装 Node.js 22:** 浏览器打开 [https://nodejs.org/zh-cn](https://nodejs.org/zh-cn) 下载 LTS 版本。下载后双击运行，一路点击“下一步”直到安装完成。
2. **安装 Git:** 打开 [https://git-scm.com/downloads/win](https://git-scm.com/downloads/win) 下载并默认安装。
3. **验证安装:** 打开一个全新的 PowerShell 窗口，输入 `node -v`，如果出现 `v22.x.x` 说明安装成功。

### 步骤 2: 运行国内优化安装命令
在 PowerShell 中，复制粘贴以下命令并回车：

```powershell
npm install -g openclaw-cn@latest --registry=https://registry.npmmirror.com
```

### 步骤 3: 启动配置向导
安装完成后，输入以下命令完成初始化设定（选择语言等）：

```powershell
openclaw onboard --install-daemon
```

---

## ✅ 安装后常用命令速查

| 命令 | 说明 |
|------|------|
| `openclaw onboard` | 重新运行配置向导 |
| `openclaw dashboard` | 在浏览器打开图形化控制面板 |
| `openclaw gateway start` | 启动后台服务 |
| `openclaw gateway stop` | 停止后台服务 |
| `openclaw doctor` | 自动诊断并修复常见错误 |

---

## ❓ 常见问题排查 (FAQ)

### Q: PowerShell 报错提示“无法加载脚本”或“执行策略”拦截？
**A:** 这是 Windows 默认的安全限制。
1. 点击“开始”菜单搜索 `PowerShell`。
2. 右键点击它，选择**“以管理员身份运行”**。
3. 运行以下命令，遇到提示输入 `Y` 并回车：
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
4. 关掉窗口，重新打开普通的 PowerShell 继续安装。

### Q: 安装提示 Node.js 版本不对？
**A:** OpenClaw 严格要求 Node.js >= 22。请前往 [https://nodejs.org](https://nodejs.org) 下载最新的 LTS 版本并重新安装以覆盖旧版本。

### Q: 运行 `gateway install` 命令失败？
**A:** Windows 环境下可能遇到系统任务权限问题，请直接改用 `openclaw gateway start` 命令代替。

### Q: 安装完成后怎么使用？
**A:** 在命令行中输入 `openclaw dashboard` 并回车，即可在浏览器中打开控制面板。

---

## 🔒 安全提示

- OpenClaw 是前沿实验性软件，请勿在存有敏感数据的设备上运行。
- 日常使用**不要**以管理员身份运行（修改执行策略时除外）。
- 绝对不要将网关端口暴露到公网。