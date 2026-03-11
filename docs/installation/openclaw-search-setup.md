# OpenClaw 搜索引擎配置指南（可选）

配置搜索引擎后，你的 AI 助手就能上网搜索最新信息来回答你的问题。**这是一个可选功能**——不配也完全不影响正常聊天，只是 AI 无法获取实时信息（比如今天的天气、最新的新闻等）。

> 💡 **提示：** 如果你暂时不需要 AI 上网搜索，可以完全跳过本指南。以后需要了再来配置。

---

## ✅ 前置条件

- ✅ **OpenClaw 已安装并配置** — 运行 `openclaw doctor` 全绿
- ✅ **能正常和 AI 聊天** — 基础配置已完成

---

## 🤔 搜索引擎是什么？

简单来说，就是让你的 AI 助手能"上网查东西"。

**没配搜索引擎时：** AI 只能根据它训练时学到的知识回答你，不知道最新发生的事
**配了搜索引擎后：** AI 可以实时搜索网页，给你最新、最准确的答案

---

## 📋 可选的搜索引擎

OpenClaw 支持多种搜索引擎，你只需要选一个：

| 搜索引擎 | 特点 | 适合人群 | 费用 |
| :--- | :--- | :--- | :--- |
| **Kimi（月之暗面）** | 国内直连，中文搜索好 | 🇨🇳 国内用户首选 | 有免费额度 |
| **Brave Search** | 国际搜索引擎，结果质量高 | 需要科学上网 | 有免费额度 |
| **Perplexity** | AI 增强搜索，结果精准 | 需要科学上网 | 付费 |
| **Gemini** | Google 搜索能力 | 需要 Gemini API Key | 有免费额度 |

> 💡 **国内用户推荐：** 如果你已经在用 Kimi（月之暗面）的 API Key，直接用 Kimi 搜索最简单——不需要额外申请新的 Key。

---

## 🚀 配置方法

### 方式一：使用配置向导（最简单）

```bash
openclaw configure --section web
```

向导会引导你选择搜索引擎并填入 API Key。

---

### 方式二：手动配置

如果你更喜欢直接编辑配置文件，按照你选择的搜索引擎来配置：

#### Kimi（国内用户推荐）

如果你已经有月之暗面的 API Key（在初始配置时选了 Moonshot AI），可以直接复用：

```json5
// ~/.openclaw/openclaw.json
{
  "tools": {
    "web": {
      "search": {
        "provider": "kimi",
        "kimi": {
          "apiKey": "你的Moonshot API Key"
        }
      }
    }
  }
}
```

> 💡 **提示：** 如果你在初始配置时选了 Kimi/Moonshot 作为 AI 模型，你已经有 API Key 了。去 [platform.moonshot.cn](https://platform.moonshot.cn) 可以找到它。

#### Brave Search

1. 访问 [brave.com/search/api](https://brave.com/search/api/)，注册账号
2. 选择 **"Data for Search"** 计划（注意：不要选 "Data for AI"，那个不兼容）
3. 生成 API Key

```json5
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "apiKey": "你的Brave API Key"
      }
    }
  }
}
```

#### Gemini

如果你已经有 Gemini API Key：

```json5
{
  "tools": {
    "web": {
      "search": {
        "provider": "gemini",
        "gemini": {
          "apiKey": "你的Gemini API Key"
        }
      }
    }
  }
}
```

---

### ❓ 常见问题

**Q：我已经选了 Kimi 作为 AI 模型，还需要单独申请搜索引擎的 Key 吗？**
A：不需要！直接复用同一个 Moonshot API Key 就行。

**Q：配置搜索引擎会产生额外费用吗？**
A：搜索引擎调用会消耗 API 额度，但通常很少。大部分对话不需要搜索，AI 会自动判断什么时候需要上网查。

**Q：我可以不配搜索引擎吗？**
A：完全可以。搜索只是一个增强功能。不配也不影响 AI 聊天。

---

## 🛠️ 验证配置

配置完成后，重启网关：

```bash
openclaw gateway restart
```

然后试着问 AI 一个需要实时信息的问题，比如"今天北京天气怎么样"。如果 AI 能给出最新的天气信息，说明搜索引擎配置成功！

如果 AI 说"我没有最新信息"或者报错，运行 `openclaw doctor` 检查搜索配置是否正确。

---

## 📋 常用命令速查

| 命令 | 作用 |
| :--- | :--- |
| `openclaw configure --section web` | 配置搜索引擎（向导模式） |
| `openclaw doctor` | 检查所有配置是否正常 |
| `openclaw gateway restart` | 重启网关使配置生效 |

---

*有问题？随时告诉我，我来帮你配置。*
