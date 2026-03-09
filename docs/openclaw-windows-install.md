# OpenClaw Windows 安装指南

本文档作为 Dify 知识库的数据源，用于指导用户在 Windows 上安装 OpenClaw。

---

## 系统要求

- 操作系统: Windows 10/11 (64位)
- CPU: 2 核以上
- 内存: 4 GB 以上
- 磁盘: 10 GB 以上可用空间
- Node.js: >= 22（重要！Node 20 会导致依赖错误）
- Git: 需要安装

---

## 方法一：一键安装脚本（推荐新手使用）

### 步骤 1: 打开 PowerShell

1. 按键盘上的 `Win + X` 键
2. 选择 "Windows PowerShell" 或 "终端"
3. 会出现一个黑色/蓝色的窗口，这就是命令行

### 步骤 2: 运行安装命令

在 PowerShell 中复制粘贴以下命令，然后按回车：

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

如果上面的命令因为网络问题失败，可以使用 CMD 方式：
1. 按 `Win + R`，输入 `cmd`，回车
2. 粘贴以下命令：

```cmd
curl -fsSL https://openclaw.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

这个脚本会自动安装 Node.js 22 和 OpenClaw，并启动配置向导。

### 步骤 3: 按照向导完成配置

安装完成后会自动启动 `openclaw onboard` 配置向导，按提示：
1. 选择语言（选中文）
2. 选择 LLM 模型提供商（推荐国内用户选 DeepSeek、Kimi 或通义千问，无需翻墙）
3. 输入对应的 API Key
4. 完成！

---

## 方法二：npm 手动安装

适合已经有 Node.js 环境的用户。

### 步骤 1: 安装 Node.js 22

1. 打开 https://nodejs.org/zh-cn
2. 下载 LTS 版本（确保是 22.x 以上）
3. 双击安装，一路"下一步"即可
4. 安装完后打开 PowerShell，输入 `node -v` 确认版本是 v22.x

### 步骤 2: 安装 Git

1. 打开 https://git-scm.com/downloads/win
2. 下载并安装，使用默认设置即可

### 步骤 3: 安装 OpenClaw

**中国大陆用户**（推荐使用国内镜像加速）：

```powershell
npm install -g openclaw --registry=https://registry.npmmirror.com
```

如果想永久切换为国内镜像：

```powershell
npm config set registry https://registry.npmmirror.com
npm install -g openclaw@latest
```

**国际用户**（默认 npm 源）：

```powershell
npm install -g openclaw@latest
```

### 步骤 4: 初始化配置

```powershell
openclaw onboard --install-daemon
```

---

## 方法三：使用国内优化版 openclaw-cn

专为中国大陆用户优化，将 GitHub 依赖改为 npm 包，全部从淘宝镜像下载，成功率 95% 以上。

```powershell
npm install -g openclaw-cn@latest --registry=https://registry.npmmirror.com
```

然后同样运行 `openclaw onboard` 完成配置。

---

## 方法四：Docker 安装（适合有经验的用户）

需要先安装 Docker Desktop for Windows。

```powershell
# 克隆仓库
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 构建并启动
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm openclaw-cli onboard
docker compose up -d openclaw-gateway
```

---

## 常见 LLM 配置

OpenClaw 支持多种大模型，国内用户推荐使用无需翻墙的国产模型：

### DeepSeek（推荐性价比最高）

```powershell
openclaw config set llm.provider "deepseek"
openclaw config set llm.deepseek.apiKey "你的API Key"
```

### 通义千问 (Qwen)

```powershell
openclaw config set llm.provider "qwen"
openclaw config set llm.qwen.apiKey "你的API Key"
```

### Kimi (月之暗面)

```powershell
openclaw config set llm.provider "kimi"
openclaw config set llm.kimi.apiKey "你的API Key"
```

### 智谱 GLM

```powershell
openclaw config set llm.provider "glm"
openclaw config set llm.glm.apiKey "你的API Key"
```

---

## 安装后常用命令

| 命令 | 说明 |
|------|------|
| `openclaw onboard` | 重新运行配置向导 |
| `openclaw dashboard` | 打开 Web 控制面板 |
| `openclaw gateway start` | 启动后台服务 |
| `openclaw gateway stop` | 停止后台服务 |
| `openclaw doctor` | 自动诊断和修复问题 |
| `openclaw config list` | 查看当前配置 |

---

## 常见问题

### Q: 安装命令卡住或下载很慢？
A: 国内网络问题，使用淘宝镜像：
```powershell
npm install -g openclaw --registry=https://registry.npmmirror.com
```
或使用 openclaw-cn 版本。

### Q: 提示 Node.js 版本不对？
A: OpenClaw 要求 Node.js >= 22。请到 https://nodejs.org 下载最新 LTS 版本重新安装。

### Q: `gateway install` 命令失败？
A: Windows 上可能遇到 schtasks 权限问题，改用 `openclaw gateway start` 代替。

### Q: 如何设置每日费用上限？
A: 运行以下命令设置每日 10 元上限（使用美元单位）：
```powershell
openclaw config set llm.limits.dailySpend 10
```
超限后会自动切换到更便宜的模型。

### Q: PowerShell 提示"无法加载脚本"或"执行策略"问题？
A: 以管理员身份打开 PowerShell，运行：
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
然后重新执行安装命令。

### Q: 安装完成后如何启动？
A: 运行 `openclaw dashboard` 打开控制面板，或直接在命令行中使用 `openclaw` 命令。

---

## 安全提示

- OpenClaw 是实验性软件，不要在存有敏感数据的设备上安装
- 不要以管理员身份运行（除了修改执行策略时）
- 安装社区插件前请先审查其代码
- 不要将 gateway 暴露到公网
