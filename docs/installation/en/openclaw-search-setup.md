# OpenClaw Search Engine Setup Guide (Optional)

Once you configure a search engine, your AI assistant can search the web for the latest information. **This is an optional feature** — skipping it won't affect normal chatting, but the AI won't be able to look up real-time information (like today's weather or the latest news).

> 💡 **Tip:** If you don't need web search right now, skip this guide entirely. You can always come back and set it up later.

---

## ✅ Prerequisites

- ✅ **OpenClaw is installed and configured** — `openclaw doctor` shows all green
- ✅ **You can chat with the AI normally** — basic setup is complete

---

## 🤔 What Does This Do?

In simple terms, it lets your AI assistant "search the internet."

**Without search:** The AI can only answer from its training data — it doesn't know about recent events
**With search:** The AI can search the web in real time, giving you the latest and most accurate answers

---

## 📋 Available Search Engines

OpenClaw supports several search engines. You only need to pick one:

| Search Engine | Strengths | Cost |
| :--- | :--- | :--- |
| **Brave Search** | High quality results, privacy-focused | Free tier available (2,000 queries/month) |
| **Gemini** | Google's search power, multimodal | Free tier if you have a Gemini API key |
| **Perplexity** | AI-enhanced search, precise results | Paid |

> 💡 **Recommendation:** **Brave Search** is a great default choice — free tier is generous, results are high quality, and setup is straightforward.

---

## 🚀 How to Configure

### Method 1: Use the Configuration Wizard (Easiest)

```bash
openclaw configure --section web
```

The wizard will guide you through choosing a search engine and entering your API key.

---

### Method 2: Manual Configuration

If you prefer editing the config file directly, follow the instructions for your chosen search engine:

#### Brave Search (Recommended)

1. Go to [brave.com/search/api](https://brave.com/search/api/) and create an account
2. Choose the **"Data for Search"** plan (Important: do NOT choose "Data for AI" — it's not compatible)
3. Generate an API key

```json5
// ~/.openclaw/openclaw.json
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "apiKey": "your-brave-api-key"
      }
    }
  }
}
```

#### Gemini

If you already have a Gemini API key:

```json5
{
  "tools": {
    "web": {
      "search": {
        "provider": "gemini",
        "gemini": {
          "apiKey": "your-gemini-api-key"
        }
      }
    }
  }
}
```

---

### ❓ FAQ

**Q: Does search cost extra money?**
A: Search calls do consume API credits, but typically very little. Most conversations don't need search — the AI automatically decides when to look something up.

**Q: Can I skip search engine setup?**
A: Absolutely. Search is an enhancement. Not configuring it doesn't affect AI chatting at all.

**Q: I already have a Gemini API key from the initial setup — can I reuse it for search?**
A: Yes! You can use the same Gemini API key for both the AI model and the search engine.

---

## 🛠️ Verify Your Configuration

After configuring, restart the gateway:

```bash
openclaw gateway restart
```

Then ask the AI a question that needs real-time info, like "What's the weather like in New York today?" If the AI gives you current weather data, your search engine is working!

If the AI says "I don't have the latest information" or shows an error, run `openclaw doctor` to check if the search configuration is correct.

---

## 📋 Quick Reference

| Command | What It Does |
| :--- | :--- |
| `openclaw configure --section web` | Configure search engine (wizard mode) |
| `openclaw doctor` | Check all configurations |
| `openclaw gateway restart` | Restart gateway to apply changes |

---

*Have questions? Tell me and I'll help you get it set up.*
