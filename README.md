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
