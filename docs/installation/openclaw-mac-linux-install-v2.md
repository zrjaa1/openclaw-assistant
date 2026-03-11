# OpenClaw macOS 与 Linux 安装指南

本指南帮助 Mac 和 Linux 用户安装 OpenClaw。Mac 和 Linux 的安装过程通常比 Windows 更顺利，但我们还是会详细说明每一步，遇到问题也不用慌。

---

## ✅ 开始之前：检查你的电脑是否符合要求

| 要求 | 如何检查 | 最低要求 |
| :--- | :--- | :--- |
| **操作系统** | Mac：点击左上角苹果图标 → 关于本机 | macOS 12 (Monterey) 或更高 |
| | Linux：终端运行 `cat /etc/os-release` | Ubuntu 20.04+、Debian 11+、Fedora 36+ 等主流发行版 |
| **磁盘空间** | Mac：苹果图标 → 关于本机 → 储存空间 | 至少 2GB 可用空间 |

---

## 🚀 方法一：官方一键安装脚本（推荐首选）

这是最简单的安装方式，一条命令搞定一切。

### 步骤 1：打开终端 (Terminal)

**Mac 用户：**
- 按下 `Command (⌘) + 空格键` 打开搜索框（Spotlight）
- 输入 `终端` 或 `Terminal`
- 按回车打开

**Linux 用户：**
- 按 `Ctrl + Alt + T` 打开终端
- 或者在应用列表中搜索 "Terminal"

### 步骤 2：运行安装命令

复制以下命令，粘贴到终端中，按**回车**：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

脚本会自动完成以下事情：
1. 检测是否已安装 Node.js（Mac 上会自动安装 Homebrew，如果没有的话）
2. 如果 Node.js 版本低于 22 或未安装，自动帮你安装
3. 安装 Git（如果需要）
4. 安装 OpenClaw
5. 启动配置向导

> 💡 **提示：** 整个过程可能需要 3-10 分钟，取决于网速和是否需要安装额外依赖。

### 步骤 3：确认安装成功

安装完成后，打开一个**新的**终端窗口，输入：

```bash
openclaw --version
```

看到版本号就说明成功了！🎉

---

### ❓ 方法一常见问题

**Q：Mac 弹出提示"需要安装命令行开发者工具 (Command Line Tools)"？**
A：这是 Mac 的正常提示，点击 **"安装"** 按钮，等待下载完成（可能需要几分钟）。完成后重新运行安装命令即可。

**Q：安装过程中提示需要输入密码？**
A：这是你的**电脑开机密码**（不是 Apple ID 密码）。输入时屏幕不会显示任何字符，这是正常的安全设计，输完直接按回车。

**Q：安装过程中卡住不动了？**
A：
1. 按 `Ctrl + C` 终止
2. 检查网络连接
3. 如果你在中国大陆，请尝试 [方法二（国内网络优化版）](#方法二国内网络优化版-openclaw-cn)

**Q：提示 "openclaw: command not found"？**
A：通常是 PATH 没有正确配置。请参考下方 [安装后找不到 openclaw 命令](#安装后找不到-openclaw-命令怎么办) 一节。

**Q：Linux 上提示 "Permission denied" 或 "EACCES"？**
A：这是 npm 全局安装的权限问题。请按以下步骤修复：
```bash
mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
然后重新运行安装命令。

---

## 🛡️ 方法二：国内网络优化版 (openclaw-cn)

如果你在中国大陆，方法一可能因为网络问题安装缓慢或失败。使用淘宝镜像可以大幅提高成功率。

### 步骤 1：安装 Node.js 22

**Mac 用户（使用 Homebrew）：**

如果你的 Mac 上已经有 Homebrew（在终端输入 `brew --version` 可以检查），直接运行：

```bash
brew install node
```

如果没有 Homebrew，先安装它：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装完 Homebrew 后再运行 `brew install node`。

> 💡 **提示：** 如果不想装 Homebrew，也可以直接从 [nodejs.org/zh-cn](https://nodejs.org/zh-cn) 下载 Mac 安装包。

**Linux 用户（Ubuntu / Debian）：**

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Linux 用户（Fedora / RHEL）：**

```bash
sudo dnf install nodejs
```

**验证安装：** 打开新终端，输入 `node -v`，看到 `v22.x.x` 或更高即可。

---

### 步骤 2：安装 OpenClaw（国内镜像）

```bash
npm install -g openclaw-cn@latest --registry=https://registry.npmmirror.com
```

> ⚠️ **Mac/Linux 提示 "Permission denied"？** 在命令前加 `sudo`：
> ```bash
> sudo npm install -g openclaw-cn@latest --registry=https://registry.npmmirror.com
> ```
> 系统会要求输入你的电脑开机密码。

### 步骤 3：启动配置向导

```bash
openclaw onboard --install-daemon
```

---

## 🔧 安装后找不到 openclaw 命令怎么办？

### 快速诊断

```bash
node -v
npm -v
npm prefix -g
echo "$PATH"
```

检查 `npm prefix -g` 输出的路径（比如 `/usr/local/lib` 或 `/Users/你的用户名/.npm-global`）后面加上 `/bin`，这个完整路径是否出现在 `echo "$PATH"` 的输出中。

### 修复方法

如果没在 PATH 里，需要手动添加。根据你用的 shell：

**Mac（zsh，默认）：**
```bash
echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Linux（bash，默认）：**
```bash
echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

然后再试 `openclaw --version`。

---

## ✅ 安装后常用命令速查

| 命令 | 说明 |
| :--- | :--- |
| `openclaw --version` | 查看 OpenClaw 版本 |
| `openclaw onboard` | 重新运行配置向导 |
| `openclaw dashboard` | 在浏览器打开图形化控制面板 |
| `openclaw doctor` | 自动诊断常见问题 |
| `openclaw gateway start` | 启动后台服务 |
| `openclaw gateway stop` | 停止后台服务 |
| `openclaw gateway status` | 查看后台服务状态 |
| `openclaw logs --follow` | 实时查看运行日志 |

---

## ❓ 综合常见问题

**Q：安装成功了，下一步该做什么？**
A：运行 `openclaw onboard` 完成初始配置（选择 AI 模型、填入 API Key 等）。如果你需要帮助，告诉我你在哪一步。

**Q：Mac 上用 Homebrew 安装的 Node.js 是不是最新版？**
A：Homebrew 会安装当前最新的 LTS 版本。运行 `node -v` 确认是 22.x 或更高即可。如果版本低了，运行 `brew upgrade node`。

**Q：我用的是 M1/M2/M3 芯片的 Mac，有兼容问题吗？**
A：没有。OpenClaw 完全兼容 Apple Silicon（M 系列芯片）。

**Q：Linux 上可以用 Docker 安装吗？**
A：可以。OpenClaw 提供了 Docker 镜像，但对于大多数个人用户来说，直接安装比 Docker 更简单。如果你熟悉 Docker 并且有特定需求，可以参考 OpenClaw 官方文档的 Docker 部分。

---

## 🔒 安全提示

- OpenClaw 是前沿实验性软件，建议在个人电脑上使用
- 绝对不要将网关端口暴露到公网
- API Key 是敏感信息，不要分享给他人
- 日常使用不需要 `sudo`（只有安装全局 npm 包时可能需要）

---

*有问题？随时告诉我你在哪一步卡住了，我来帮你。*
