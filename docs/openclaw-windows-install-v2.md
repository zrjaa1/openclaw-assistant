# OpenClaw Windows 安装指南

本指南将帮助你在 Windows 电脑上安装 OpenClaw。我们会尽量详细地说明每一步，遇到问题不要慌，大部分问题都有解决办法。

---

## ✅ 开始之前：检查你的电脑是否符合要求

在安装之前，请先确认你的电脑满足以下条件：

| 要求 | 如何检查 | 最低要求 |
| :--- | :--- | :--- |
| **操作系统** | 按 `Win + I` 打开设置 → 系统 → 关于 | Windows 10（64位）或 Windows 11 |
| **系统类型** | 同上，查看"系统类型"一栏 | 必须是 **64 位操作系统** |
| **磁盘空间** | 打开"此电脑"查看 C 盘剩余空间 | 至少 2GB 可用空间 |

> ⚠️ **不支持的系统：** 如果你的电脑是 Windows 7、Windows 8/8.1，或者是 32 位系统，很遗憾 OpenClaw 无法在上面运行。建议升级到 Windows 10 或 Windows 11 后再尝试安装。

> 💡 **提示：** 不确定自己的系统版本？按键盘上的 `Win + R`，输入 `winver`，按回车，弹出的窗口会显示你的 Windows 版本。

---

## 🚀 方法一：官方一键安装脚本（推荐首选）

这是最简单的安装方式，脚本会自动帮你检测环境、安装依赖、配置 OpenClaw。

### 步骤 1：打开 PowerShell

1. 按住键盘上的 `Win` 键（键盘左下角带 Windows 图标的键），然后按 `X` 键
2. 在弹出的菜单中，点击 **Windows PowerShell** 或 **终端 (Terminal)**
3. 屏幕上会出现一个深色背景的命令行窗口

> 💡 **提示：** 如果菜单里没有 PowerShell 选项，也可以点击"开始"菜单，搜索 `PowerShell`，点击打开。

> ⚠️ **注意：** 这一步**不需要**以管理员身份运行。用普通模式打开即可。

### 步骤 2：运行安装命令

复制下方这行代码：

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

然后在 PowerShell 窗口中**右键粘贴**（PowerShell 里右键 = 粘贴），按下**回车键**。

> 💡 **提示：** 粘贴后如果看起来什么都没发生，别担心，请耐心等待。安装过程需要从网络下载文件，可能需要几分钟。

脚本会自动完成以下事情：
1. 检测你的电脑是否已安装 Node.js（OpenClaw 的运行环境）
2. 如果没有，自动帮你安装 Node.js 22
3. 安装 OpenClaw 本体
4. 启动配置向导

### 步骤 3：确认安装成功

安装完成后，**关闭当前的 PowerShell 窗口，重新打开一个新的**（这很重要，新窗口才能识别新安装的命令），然后输入：

```powershell
openclaw --version
```

如果看到版本号（比如 `1.x.x`），恭喜你，安装成功！🎉

---

### ❓ 方法一常见问题

**Q：运行命令后提示"无法加载脚本"、"执行策略"或 "is not digitally signed"？**
A：这是 Windows 默认的安全限制。请按以下步骤解除：
1. 关闭当前 PowerShell 窗口
2. 点击"开始"菜单，搜索 `PowerShell`
3. **右键**点击 PowerShell，选择 **"以管理员身份运行"**
4. 在打开的窗口里输入以下命令，遇到提示输入 `Y` 并回车：
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
5. 关闭这个管理员窗口
6. 重新打开一个**普通的** PowerShell，重新运行安装命令

> ⚠️ **注意：** 修改执行策略只需要做一次。以后安装其他东西不需要再改了。

**Q：安装过程中卡住不动了，进度条不走了？**
A：可能是网络问题（下载 Node.js 或 OpenClaw 包时卡住了）。
1. 按 `Ctrl + C` 终止当前操作
2. 检查你的网络连接是否正常
3. 如果你在中国大陆，国际网络可能不稳定，请尝试 [方法二（国内网络优化版）](#方法二国内网络优化版-openclaw-cn)
4. 如果有科学上网工具，确保 PowerShell 也走了代理（有些代理只对浏览器生效）

**Q：提示 "npm error spawn git ENOENT" 或者找不到 git？**
A：你需要先安装 Git。请打开浏览器访问 [https://git-scm.com/downloads/win](https://git-scm.com/downloads/win)，下载并安装（一路点"Next"即可）。安装完 Git 后，**关闭 PowerShell 重新打开**，再运行安装命令。

**Q：提示 "openclaw 不是内部或外部命令" 或 "is not recognized"？**
A：这通常是 PATH 环境变量没有正确配置。请参考下方 [安装后找不到 openclaw 命令](#安装后找不到-openclaw-命令怎么办) 一节。

**Q：安装命令执行了但好像什么都没装成功？**
A：在新的 PowerShell 窗口中运行以下命令检查：
```powershell
node -v
npm -v
openclaw --version
```
把这三个命令的输出结果告诉我，我可以帮你判断哪一步出了问题。

---

## 🛡️ 方法二：国内网络优化版 (openclaw-cn)

如果你在中国大陆，方法一可能因为网络原因速度很慢或者失败。这个方案使用国内淘宝镜像下载，速度快且成功率高。

### 步骤 1：安装 Node.js 22

OpenClaw 需要 Node.js 22 或更高版本才能运行。如果你还没有安装，请选择以下任意一种方式：

**方式 A：用 winget 安装（最简单，Windows 10 1709+ 自带）**

打开 PowerShell，输入：

```powershell
winget install OpenJS.NodeJS.LTS
```

> 💡 **提示：** `winget` 是 Windows 自带的软件包管理器。如果提示 `winget 不是内部或外部命令`，说明你的 Windows 版本较旧，请用方式 B。

**方式 B：从官网手动下载安装**

1. 打开浏览器，访问 [https://nodejs.org/zh-cn](https://nodejs.org/zh-cn)
2. 点击 **LTS（长期支持版）** 的下载按钮（确认版本号是 22.x 或更高）
3. 下载后双击运行安装程序
4. 安装过程中一路点击 **"Next"**（下一步），不需要修改任何选项
5. 最后点击 **"Finish"** 完成安装

> ⚠️ **注意：** 安装完成后**必须关闭所有 PowerShell 窗口再重新打开一个新的**，否则系统不会识别刚安装的 Node.js。

**验证安装：** 打开一个全新的 PowerShell 窗口，输入：

```powershell
node -v
```

如果看到 `v22.x.x` 或更高版本号，说明 Node.js 安装成功。

---

### ❓ Node.js 安装常见问题

**Q：`node -v` 显示的版本号低于 22（比如 v18 或 v20）？**
A：OpenClaw 严格要求 Node.js 22 或更高版本。请重新下载安装最新的 LTS 版本，新安装会自动覆盖旧版本。

**Q：`node -v` 提示"不是内部或外部命令"？**
A：说明安装没成功，或者 PATH 没配置好。请检查：
1. 确认你是在**新打开的** PowerShell 窗口中运行的（不是安装前打开的旧窗口）
2. 如果还是不行，尝试重新安装 Node.js，安装时注意勾选 "Add to PATH" 选项

**Q：winget 安装 Node.js 时提示需要同意协议？**
A：输入 `Y` 并回车确认即可。

---

### 步骤 2：安装 Git

OpenClaw 的一些依赖需要 Git。如果你还没有安装：

1. 打开浏览器，访问 [https://git-scm.com/downloads/win](https://git-scm.com/downloads/win)
2. 下载后双击运行，安装过程中**所有选项保持默认**，一路点 "Next" 直到完成

> 💡 **提示：** 不确定是否已经安装了 Git？打开 PowerShell 输入 `git --version`，如果看到版本号就说明已经有了，可以跳过这步。

---

### 步骤 3：安装 OpenClaw（国内镜像）

在 PowerShell 中，复制粘贴以下命令并回车：

```powershell
npm install -g openclaw-cn@latest --registry=https://registry.npmmirror.com
```

这个命令会从淘宝镜像下载 OpenClaw，速度会快很多。

> 💡 **提示：** 安装过程可能需要 2-5 分钟，取决于网速。如果看到一些 `WARN` 警告，通常可以忽略。只要最后没有 `ERR!` 错误就说明安装成功了。

---

### 步骤 4：验证安装

关闭 PowerShell，重新打开一个新的，输入：

```powershell
openclaw --version
```

看到版本号就说明安装成功！🎉 接下来运行配置向导：

```powershell
openclaw onboard --install-daemon
```

> 💡 **提示：** `--install-daemon` 参数会让 OpenClaw 安装为后台服务，这样关掉 PowerShell 窗口后它还会继续运行。

---

### ❓ 方法二常见问题

**Q：`npm install` 报错 "EACCES" 或权限不足？**
A：尝试用管理员身份运行 PowerShell 再执行安装命令。

**Q：安装过程中出现大量红色 `ERR!` 错误？**
A：请把完整的错误信息复制给我，我帮你分析。常见原因包括：
- Node.js 版本太低（必须 >= 22）
- 网络连接中断
- 磁盘空间不足

**Q：`openclaw-cn` 和普通的 `openclaw` 有什么区别？**
A：功能完全一样。`openclaw-cn` 只是优化了下载源，让中国大陆用户安装更快更稳定。

---

## 🛠️ 方法三：使用 WSL2（高级用户推荐）

如果你有一定的技术基础，OpenClaw 官方**强烈推荐**在 Windows 上使用 WSL2（Windows Subsystem for Linux，Windows 下的 Linux 子系统）来运行。WSL2 的兼容性更好，遇到的问题也更少。

> 💡 **提示：** 如果你不知道 WSL 是什么，或者觉得这听起来很复杂，请直接跳过这个方法，使用方法一或方法二即可。

### 步骤 1：安装 WSL2

打开 **管理员模式** 的 PowerShell（右键 PowerShell → 以管理员身份运行），输入：

```powershell
wsl --install
```

系统会自动安装 WSL2 和 Ubuntu。安装完成后**需要重启电脑**。

> ⚠️ **注意：** 这个命令需要 Windows 10 版本 2004 或更高版本。如果提示不支持，说明你的 Windows 版本太旧，需要先更新系统。

### 步骤 2：配置 Ubuntu

重启后，在开始菜单搜索 `Ubuntu` 并打开。首次启动会要求你设置用户名和密码（这是 Linux 系统的用户名密码，和 Windows 登录密码无关）。

### 步骤 3：在 WSL2 中安装 OpenClaw

在 Ubuntu 终端里运行：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

后续的配置步骤和普通 Linux 安装相同。

---

## 🔧 安装后找不到 openclaw 命令怎么办？

这是 Windows 上最常见的问题之一。通常是因为 npm 安装的命令没有被加入到系统的 PATH 环境变量中。

### 快速诊断

打开一个新的 PowerShell 窗口，依次运行这三个命令：

```powershell
node -v
npm -v
npm prefix -g
```

**情况 1：** `node -v` 或 `npm -v` 就报错了
→ Node.js 没装好，请回到上面重新安装 Node.js

**情况 2：** 前两个正常，`npm prefix -g` 输出了一个路径（比如 `C:\Users\你的用户名\AppData\Roaming\npm`）
→ 需要把这个路径加到 PATH 里，请按以下步骤操作：

### 手动添加 PATH

1. 按 `Win + I` 打开 Windows 设置
2. 搜索 **"环境变量"**，点击 **"编辑系统环境变量"**
3. 在弹出的窗口中，点击下方的 **"环境变量"** 按钮
4. 在**上半部分**（"用户变量"）中，找到 `Path`，双击打开
5. 点击 **"新建"**，粘贴 `npm prefix -g` 命令输出的路径
6. 点击 **"确定"** 保存所有窗口
7. **关闭所有 PowerShell 窗口，重新打开一个新的**
8. 运行 `openclaw --version` 验证

> 💡 **提示：** 如果你不确定具体操作步骤，可以截图给我，我来指导你。

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
A：运行 `openclaw onboard` 完成初始配置（选择 AI 模型、填入 API Key 等）。如果你需要帮助，告诉我你在哪一步，我来指导。

**Q：我的电脑配置很低，OpenClaw 会不会很卡？**
A：OpenClaw 本身占用资源很少（它只是一个消息中转站）。AI 推理是在云端进行的，所以你的电脑配置基本不影响使用体验。

**Q：可以安装在移动硬盘或 U 盘上吗？**
A：不建议。OpenClaw 需要全局安装到系统路径，而且需要作为后台服务运行。安装在可移动存储设备上可能导致各种路径和权限问题。

**Q：需要关闭杀毒软件吗？**
A：正常情况下不需要。但如果安装过程中杀毒软件弹出拦截提示，可以选择"允许"或暂时关闭实时保护，安装完成后再打开。

**Q：公司电脑有管理策略限制，装不了怎么办？**
A：如果公司的 IT 策略限制了软件安装，你可能需要联系 IT 部门申请权限。具体限制包括：
- 禁止运行 PowerShell 脚本 → 需要 IT 修改执行策略
- 禁止安装全局 npm 包 → 需要 IT 开放 npm 权限
- 代理/防火墙拦截下载 → 需要 IT 加白名单
如果公司不允许安装，建议在个人电脑上使用。

**Q：安装完成后可以卸载 Node.js 吗？**
A：不可以。Node.js 是 OpenClaw 的运行环境，删掉 Node.js 后 OpenClaw 就无法运行了。

---

## 🔒 安全提示

- OpenClaw 是前沿实验性软件，建议在专用或个人电脑上使用
- 日常使用**不需要**以管理员身份运行（只有修改执行策略时才需要）
- 绝对不要将网关端口暴露到公网
- API Key 是敏感信息，不要分享给他人
