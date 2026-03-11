# OpenClaw 更新与升级指南

OpenClaw 会持续发布新版本，修复问题和增加功能。本指南教你如何安全地更新到最新版本。

> 💡 **提示：** 更新只会替换程序本身，你的配置文件、API Key、聊天记录都不会丢失。

---

## 🚀 如何更新

根据你最初的安装方式，选择对应的更新命令：

### 方式一：重新运行安装脚本（最简单，推荐）

不管你之前是怎么安装的，重新运行安装脚本都可以更新：

**Mac / Linux：**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

**Windows (PowerShell)：**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

> 💡 **提示：** 加 `--no-onboard` 可以跳过配置向导（你的配置已经好了，不需要再配一次）。

### 方式二：使用 npm 更新

**标准安装：**
```bash
npm update -g openclaw
```

**国内镜像安装：**
```bash
npm update -g openclaw-cn --registry=https://registry.npmmirror.com
```

---

## ✅ 更新后验证

更新完成后，运行以下命令确认一切正常：

```bash
openclaw --version
openclaw doctor
openclaw gateway restart
```

1. `--version` — 确认版本号已更新
2. `doctor` — 全面体检，检查配置是否需要迁移
3. `gateway restart` — 重启网关让新版本生效

> 💡 **提示：** `openclaw doctor` 会自动修复一些版本升级带来的配置变化，所以更新后一定要运行一次。

---

## ❓ 常见问题

**Q：更新后原来的配置会丢失吗？**
A：不会。你的配置保存在 `~/.openclaw/` 目录下，更新只替换程序本身。

**Q：更新后机器人不工作了怎么办？**
A：
1. 先运行 `openclaw doctor`，它会检测并修复大部分问题
2. 运行 `openclaw gateway restart` 重启网关
3. 如果还不行，查看日志 `openclaw logs --follow`

**Q：想回退到旧版本怎么办？**
A：安装指定版本即可（把 `版本号` 换成你想要的，比如 `1.2.3`）：
```bash
npm install -g openclaw@版本号
openclaw doctor
openclaw gateway restart
```

**Q：怎么知道有没有新版本？**
A：OpenClaw 启动时会自动检查更新并在日志中提示。你也可以随时运行安装脚本或 `npm update` 来获取最新版。

---

*更新遇到问题？把 `openclaw doctor` 的输出发给我，我来帮你排查。*
