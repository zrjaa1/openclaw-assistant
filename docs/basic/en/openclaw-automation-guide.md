# OpenClaw Automation Tips: Let Your AI Assistant Reach Out to You

Did you know? OpenClaw isn't just a chatbot that waits for your questions — you can have it send you messages on a schedule! Like a daily weather forecast every morning, or a reminder every afternoon.

Setting it up couldn't be easier: you don't need to learn any technical commands. Just tell your AI assistant what you want in plain English.

---

## ✅ Prerequisites

- ✅ OpenClaw is set up and you can chat normally
- ✅ You've connected at least one chat platform (Telegram, Discord, WhatsApp, Slack, etc.)
- ✅ The gateway is running in the background (you should have run `openclaw gateway install`)

---

## 💡 How to Use It: Just Tell the AI!

You just tell your AI assistant what you want in a normal chat message, and it handles the rest. Here are some examples you can copy and use:

---

### Daily Weather Report

Tell the AI:

"Set up a daily task at 8 AM to check the weather in New York and send it to me."

The AI will automatically create a scheduled task that checks the weather every morning and sends the results to your current chat.

---

### Daily News Summary

Tell the AI:

"Every morning at 9 AM, search for today's tech news and give me a short summary."

The AI will search for the latest tech news daily and send you a summary.

(Note: This requires a search engine to be configured.)

---

### Work Reminders

Tell the AI:

"Remind me to write my daily report every weekday at 5:30 PM."

Or more specifically:

"Every Friday at 4 PM, remind me to submit my weekly report."

---

### One-Time Reminders

Tell the AI:

"Remind me about my meeting in 20 minutes."

Or:

"Remind me to call the client today at 3 PM."

One-time reminders automatically delete themselves after firing — they won't repeat.

---

### Health Reminders

Tell the AI:

"Every day at noon, remind me to stand up and stretch. Give me a different stretching exercise each time."

---

### Learning Log

Tell the AI:

"Every night at 9 PM, ask me what I learned today and help me write it down."

---

## 📋 Tips for Best Results

1. Be specific about timing — "every day at 8 AM" is better than "every morning"
2. Be specific about what to do — "check the weather in New York" is clearer than "check the weather"
3. You can adjust anytime — just tell the AI "change my weather reminder to 7 AM"
4. You can cancel anytime — just say "cancel the daily weather reminder" or "delete that scheduled task"
5. One-time reminders work too — "remind me in 20 minutes" is perfectly fine

---

## ❓ FAQ

**Q: I set up a scheduled task but didn't receive the message?**
A: Make sure your OpenClaw gateway is still running. Scheduled tasks need the gateway running in the background to fire on time. Ask the AI: "Check if the gateway is running."

**Q: Can I have multiple scheduled tasks at the same time?**
A: Absolutely! You can set up as many different tasks as you want — they don't interfere with each other.

**Q: Do scheduled tasks use API credits?**
A: Yes, each time a task fires, the AI runs once and uses a small amount of credits. Daily usage is minimal.

**Q: How does it know my timezone?**
A: OpenClaw uses your computer's timezone by default. If you're in the US Eastern time zone, saying "8 AM" means 8 AM Eastern.

**Q: How do I see what tasks I've set up?**
A: Just ask the AI: "What scheduled tasks do I have?" and it will list them for you.

---

There's a lot more you can do! Try describing any automation you'd like in your own words — the AI will do its best to make it happen.
