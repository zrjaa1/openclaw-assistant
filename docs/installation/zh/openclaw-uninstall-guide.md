# OpenClaw 卸载指南

如果你想完全卸载小龙虾（OpenClaw），按照下面的步骤操作就行。卸载不会影响你电脑上的其他软件。

---

## 最简单的方式（推荐）

如果你的 openclaw 命令还能用，只需要一行命令就能完全卸载：

复制下面这行命令粘贴到终端里：
openclaw uninstall

系统会问你几个确认问题，按提示选择就行。

如果想跳过所有确认，直接全部删除：
openclaw uninstall --all --yes

---

## 手动卸载步骤

如果上面的命令不能用了，可以手动一步步卸载：

1. 先停止后台服务

复制下面的命令：
openclaw gateway stop
openclaw gateway uninstall

2. 删除配置和数据

Windows 用户：
打开文件管理器，在地址栏输入 %USERPROFILE%\.openclaw ，回车后删除整个文件夹。

Mac/Linux 用户：
复制下面这行命令：
rm -rf ~/.openclaw

3. 删除程序本身

复制下面这行命令：
npm rm -g openclaw

如果你当初用的是国内镜像安装的：
npm rm -g openclaw-cn

---

## Windows 用户额外注意

如果卸载后发现后台服务还在运行，可以手动删除计划任务：

按 Win + X 打开 PowerShell（管理员），复制下面的命令：
schtasks /Delete /F /TN "OpenClaw Gateway"

---

## Mac 用户额外注意

如果卸载后发现后台服务还在运行：

复制下面的命令：
launchctl bootout gui/$UID/ai.openclaw.gateway
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist

如果你安装过 macOS 桌面应用，还需要删除它：
rm -rf /Applications/OpenClaw.app

---

## Linux 用户额外注意

如果卸载后发现后台服务还在运行：

复制下面的命令：
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload

---

## 常见问题

Q：卸载后能重新安装吗？
A：当然可以！随时重新安装，就像第一次安装一样。之前的配置会被清除，需要重新配置。

Q：卸载会影响我电脑上的其他软件吗？
A：不会。卸载只会删除小龙虾自己的文件，不会动你电脑上的任何其他东西。

Q：我想保留配置，只更新程序可以吗？
A：可以！那你不需要卸载，只需要更新就行。请参考更新指南。

Q：卸载后 Node.js 也要删吗？
A：不需要。Node.js 是独立的软件，其他程序可能也在用它。如果你确定不需要了，可以单独卸载 Node.js，但跟小龙虾的卸载是分开的。

---

卸载过程中遇到问题？把终端里的报错信息发给我，我来帮你解决。
