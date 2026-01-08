# year-decay-bot

A Telegram bot that posts a daily reminder that time is passing, the year is disappearing, and the weather is not here to help you.

It sends one message per day to a Telegram group with:
- How much of the current year is gone (with two decimals, because denial loves precision)
- A visual progress bar slowly filling up
- The daily weather forecast for Madrid
- “Feels like” temperature, openly mocked
- Available daylight, treated as a finite and dwindling resource
- Cynical, ominous commentary that escalates as the year progresses
- A special end-of-year message on December 31st

It avoids duplicate posts, resets cleanly every year, and does not attempt to motivate anyone.

---

## What this is

This is not a productivity tool.  
This is not a wellness app.  
This is not inspirational.

`year-decay-bot` exists to:
- Track time accurately
- Treat weather indifferently
- Remind you that planning is optional and time is not

Sunny days are not celebrated.  
Bad weather is not dramatized.  
Everything is treated with the same quiet contempt.

## Design philosophy

This bot is intentionally minimal.

It posts once per day, says what it has to say, and leaves.  
There is no interaction, no conversation, and no attempt to be helpful.

Silence is treated as a feature.  
Repetition is avoided deliberately.  
Tone changes gradually, without announcements.

The goal is not to shock or entertain, but to remain quietly present over long periods of time.

---

## Features

- Daily posting (once per day, enforced)
- Year progress with X.XX% precision
- Visual progress bar
- Escalating tone as the year advances
- Madrid weather (no API key required)
- Graceful, cynical handling of weather API failures
- Special December 31st “final accounting” message
- Year-on-year safe
- No duplicate messages
- No external dependencies beyond `requests`

## Non-goals

This project deliberately avoids:
- User interaction or commands
- Personalization or tracking
- Notifications or reminders
- Motivation, encouragement, or advice
- Real-time responsiveness

If you are looking for a bot that reacts, chats, or adapts to users, this is not that.

---

## Requirements

- Python 3.8+
- A Telegram bot token
- A Telegram group chat ID
- The bot added to the group with permission to send messages
- Privacy mode disabled via BotFather

---

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install requests
   ```
3. Edit the script and set:
   ```python
   BOT_TOKEN = "YOUR_BOT_TOKEN"
   CHAT_ID = "YOUR_CHAT_ID"
   ```
4. Make sure the bot is a member of the Telegram group
5. Disable privacy mode for the bot using **@BotFather**
6. Run once to test:
   ```bash
   python3 year_progress_daily_bot.py
   ```

---

## Automation (cron)

Run once per day. Midnight UTC is thematically appropriate.

Example cron entry:
```bash
0 0 * * * /usr/bin/python3 /path/to/year_progress_daily_bot.py
```

The bot will not post more than once per day, even if run multiple times.

---

## Notes

- The bot stores a small local state file to prevent duplicate posts.
- Make sure this file is ignored by git:
  ```
  year_progress_state.json
  ```
- Weather data is provided by Open-Meteo. If unavailable, the bot will comment on the failure instead of staying silent.
- The tone is intentional and will not soften over time.

---

## License

MIT License.

Do whatever you want with it.  
Just don’t expect it to be optimistic.

---

## Final note

This bot will not improve your mood, productivity, or outlook.

It exists to measure time, report conditions, and move on.
