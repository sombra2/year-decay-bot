import requests
from datetime import datetime, timezone
import math
import json
import os
import random
import calendar

# ─── CONFIG ────────────────────────────────────────────────────────────────
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = YOUR_CHAT_ID  # int, not string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "year_progress_state.json")
PHRASES_FILE = os.path.join(BASE_DIR, "phrases.json")

BAR_LENGTH = 20
MADRID_LAT = 40.4168
MADRID_LON = -3.7038

DEPRESSING_EMOJIS = ["☠️", "⌛", "🕰️", "🌑", "💀", "🥀", "⚰️", "🕳️"]

# ─── LOAD PHRASES ──────────────────────────────────────────────────────────
with open(PHRASES_FILE, "r") as f:
    PHRASES = json.load(f)

# ─── STATE ────────────────────────────────────────────────────────────────
def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def pick_non_repeating(pool, key, state):
    used = state.get(key, [])
    choices = [p for p in pool if p not in used] or pool
    choice = random.choice(choices)
    state[key] = (used + [choice])[-5:]
    return choice

# ─── UTIL ──────────────────────────────────────────────────────────────────
def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }, timeout=10)

def progress_bar(p):
    filled = math.floor((p / 100) * BAR_LENGTH)
    return "█" * filled + "░" * (BAR_LENGTH - filled)

def year_progress():
    now = datetime.now(timezone.utc)
    start = datetime(now.year, 1, 1, tzinfo=timezone.utc)
    end = datetime(now.year + 1, 1, 1, tzinfo=timezone.utc)
    return (now - start).total_seconds() / (end - start).total_seconds() * 100

def random_emoji():
    return random.choice(DEPRESSING_EMOJIS)

# ─── WEATHER ───────────────────────────────────────────────────────────────
def get_weather():
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={MADRID_LAT}&longitude={MADRID_LON}"
            "&daily=temperature_2m_max,temperature_2m_min,"
            "apparent_temperature_max,sunrise,sunset"
            "&timezone=Europe/Madrid"
        )
        d = requests.get(url, timeout=10).json()["daily"]
        return {
            "ok": True,
            "tmin": d["temperature_2m_min"][0],
            "tmax": d["temperature_2m_max"][0],
            "feels": d["apparent_temperature_max"][0],
            "sunrise": d["sunrise"][0],
            "sunset": d["sunset"][0]
        }
    except:
        return {"ok": False}

# ─── MAIN ──────────────────────────────────────────────────────────────────
def main():
    state = load_state()
    today = datetime.now(timezone.utc)
    today_key = today.strftime("%Y-%m-%d")

    if state.get("last_sent") == today_key:
        return

    # Random silence days (1–2 per month)
    month_key = today.strftime("%Y-%m")
    silence_days = state.get("silence_days", {})
    if month_key not in silence_days:
        days = calendar.monthrange(today.year, today.month)[1]
        silence_days[month_key] = random.sample(range(1, days + 1), random.randint(1, 2))
        state["silence_days"] = silence_days

    if today.day in silence_days[month_key]:
        state["last_sent"] = today_key
        save_state(state)
        return

    percent = year_progress()
    bar = progress_bar(percent)

    is_final = today.month == 12 and today.day == 31

    if is_final:
        quote = pick_non_repeating(PHRASES["year"]["final"], "year_final", state)
        title = "📆 *Year completed*"
    elif percent < 35:
        quote = pick_non_repeating(PHRASES["year"]["early"], "year_early", state)
        title = "📆 *Year progress update*"
    elif percent < 70:
        quote = pick_non_repeating(PHRASES["year"]["mid"], "year_mid", state)
        title = "📆 *Year progress update*"
    else:
        quote = pick_non_repeating(PHRASES["year"]["late"], "year_late", state)
        title = "📆 *Year progress update*"

    # Monthly ritual
    ritual = ""
    if today.day == 1:
        ritual = f"\n_{PHRASES['ritual'][0]}_\n"

    w = get_weather()

    if w["ok"]:
        daylight_hours = (
            datetime.fromisoformat(w["sunset"]) -
            datetime.fromisoformat(w["sunrise"])
        ).total_seconds() / 3600

        weather_block = (
            f"\n🌍 *Madrid weather*\n"
            f"{w['tmin']:.0f}°C – {w['tmax']:.0f}°C {random_emoji()}\n"
            f"Feels like {w['feels']:.0f}°C. "
            f"{pick_non_repeating(PHRASES['feels_like'], 'feels', state)}\n"
            f"{daylight_hours:.1f}h daylight. "
            f"{pick_non_repeating(PHRASES['daylight'], 'daylight', state)}\n"
            f"_{pick_non_repeating(PHRASES['weather']['normal'], 'weather', state)}_\n"
        )
    else:
        weather_block = (
            f"\n🌍 *Madrid weather*\n"
            f"Unavailable {random_emoji()}\n"
            f"_{pick_non_repeating(PHRASES['weather']['error'], 'weather_err', state)}_\n"
            f"_{pick_non_repeating(PHRASES['daylight_error'], 'daylight_err', state)}_\n"
        )

    message = (
        f"{title}\n\n"
        f"`{bar}`\n"
        f"*{percent:.2f}%* of the year is gone {random_emoji()}\n"
        f"{weather_block}"
        f"{ritual}\n"
        f"_{quote}_"
    )

    send(message)
    state["last_sent"] = today_key
    save_state(state)

if __name__ == "__main__":
    main()
