# OpenClaw macOS 与 Linux 极简安装指南

本文档专门指导没有技术背景的苹果 Mac 用户和 Linux 用户，在国内网络环境下顺利安装 OpenClaw。

---

## 💻 电脑配置要求

- **操作系统:** macOS (苹果电脑) 或主流 Linux 发行版 (如 Ubuntu)。
- **核心依赖:** 必须安装 **Node.js 22** 或以上版本（⚠️ 注意：使用老版本的 Node 20 会导致严重错误）。

---

## 🚀 方法一：官方一键安装脚本（推荐首选）

这是苹果和 Linux 系统上最简单的安装方式，脚本会自动下载并配置所需环境。

### 步骤 1: 打开“终端” (Terminal)
- **Mac 用户:** 按下键盘上的 `Command (⌘) + 空格键` 打开搜索框，输入 `终端` 或 `Terminal`，然后按回车打开黑色的命令行窗口。
- **Linux 用户:** 可以使用快捷键 `Ctrl + Alt + T` 打开终端。

### 步骤 2: 运行安装命令
复制下方这行代码，在刚才打开的终端窗口中粘贴，然后按下**回车键**：

```bash
curl -fsSL [https://openclaw.ai/install.sh](https://openclaw.ai/install.sh) | bash
```

如果因为国内网络问题导致进度条卡死或报错，请按 `Ctrl + C` 强制终止，并改用下方的**方法二**。

---

## 🛡️ 方法二：国内网络优化版 (openclaw-cn)

如果方法一因为网络墙的原因失败，请使用此兜底方案。本方法全部从国内淘宝镜像极速下载，极大提高成功率。

### 步骤 1: 手动安装 Node.js 22
1. 浏览器打开官方网站：https://nodejs.org/zh-cn
2. 下载 **LTS 版本** (请确保是 22.x 或更高版本)。
3. 下载后双击运行，按照提示完成安装。
4. 打开“终端”，输入 `node -v`，如果出现类似 `v22.x.x` 的字样，说明环境准备完毕。

### 步骤 2: 运行国内优化安装命令
在终端中，复制粘贴以下命令并回车（此命令使用了淘宝镜像）：

```bash
npm install -g openclaw-cn@latest --registry=[https://registry.npmmirror.com](https://registry.npmmirror.com)
```

*(💡 提示：如果在 Mac 或 Linux 上运行此命令时提示 `Permission denied` (权限被拒绝)，请在命令最前面加上 `sudo` 并输入你的电脑开机密码，即：`sudo npm install -g ...`)*

### 步骤 3: 启动配置向导
安装完成后，输入以下命令完成初始化设定（选择语言等）：

```bash
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

### Q: 安装提示 Node.js 版本不对？
**A:** OpenClaw 严格要求 Node.js >= 22。请前往 https://nodejs.org 下载最新的 LTS 版本并重新安装以覆盖旧版本。

### Q: Mac 安装时提示“需要安装命令行开发者工具 (Command Line Tools)”？
**A:** 这是 Mac 系统的正常提示。如果在运行命令时系统弹窗要求安装该工具，请点击“安装”并同意协议，等待其下载完成后，重新运行 OpenClaw 的安装命令即可。

### Q: 安装完成后怎么打开界面？
**A:** 在终端中输入 `openclaw dashboard` 并回车，即可在默认浏览器中打开控制面板。

---

## 🔒 安全提示

- OpenClaw 是前沿实验性软件，请勿在存有敏感数据的设备上运行。
- 绝对不要将网关端口暴露到公网。