import requests
from datetime import datetime, timezone, date
import math
import json
import os
import random

# ─── CONFIG ────────────────────────────────────────────────────────────────
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
STATE_FILE = "year_progress_state.json"

BAR_LENGTH = 20

MADRID_LAT = 40.4168 #set for Madrid, feel free to choose wherever you like
MADRID_LON = -3.7038

# ─── EMOJIS ────────────────────────────────────────────────────────────────
DEPRESSING_EMOJIS = [
    "☠️", "⌛", "🕰️", "🌑", "🪦", "💀", "🥀", "⚰️",
    "🕳️", "🫥", "🧠", "🩸"
]

def random_emoji():
    return random.choice(DEPRESSING_EMOJIS)

# ─── YEAR QUOTES ───────────────────────────────────────────────────────────
EARLY_QUOTES = [
    "Time waits for no one.",
    "The clock does not care.",
    "This year started without your consent.",
    "You are already spending it.",
    "The countdown has begun.",
    "Momentum belongs to time.",
    "The pace has been set.",
    "You are on borrowed hours."
]

MID_QUOTES = [
    "You are closer to the end than the beginning.",
    "Half of this year is already unreachable.",
    "The future is shrinking.",
    "Every delay is now permanent.",
    "Time has gained leverage.",
    "This is no longer early.",
    "The margin for error is gone."
]

LATE_QUOTES = [
    "Most of this year is already memory.",
    "You are running out of year.",
    "There is not much left to work with.",
    "The ending is approaching.",
    "What you did not do is now permanent.",
    "Explanations are losing value."
]

FINAL_DAY_QUOTES = [
    "This year is over. Nothing else will happen here.",
    "Whatever you meant to do belongs to last year now.",
    "You do not get to carry unfinished time forward.",
    "Everything you didn’t do is now permanent.",
    "The year is dead. It will not respond.",
    "Time has finished accounting."
]

# ─── WEATHER COMMENTARY ────────────────────────────────────────────────────
WEATHER_QUOTES = [
    "The weather will happen regardless of your plans.",
    "The sky remains indifferent.",
    "Conditions exist. Satisfaction is optional.",
    "Nature is not trying to help you.",
    "This will not improve your mood.",
    "The atmosphere continues its routine.",
    "Expect nothing from this."
]

WEATHER_ERROR_QUOTES = [
    "The sky refused to report today.",
    "The atmosphere declined comment.",
    "No data. Outcome unchanged.",
    "The weather opted out.",
    "Conditions unknown. Indifference confirmed."
]

FEELS_LIKE_QUOTES = [
    "It feels like something else. That changes nothing.",
    "Your body disagrees with the number.",
    "Reality is subjective. Discomfort is not.",
    "This is how it feels. Argue with the air.",
    "The number was optimistic."
]

DAYLIGHT_QUOTES = [
    "Available daylight remaining.",
    "This is how much light you get today.",
    "The sun is rationing itself.",
    "These are today’s usable hours.",
    "Daylight is not infinite."
]

DAYLIGHT_ERROR_QUOTES = [
    "Daylight data unavailable. Night still inevitable.",
    "The sun declined to elaborate.",
    "Light schedule unknown. Darkness unchanged."
]

# ─── TELEGRAM ───────────────────────────────────────────────────────────────
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload, timeout=10)

# ─── TIME / PROGRESS ────────────────────────────────────────────────────────
def year_progress_percentage():
    now = datetime.now(timezone.utc)
    year_start = datetime(now.year, 1, 1, tzinfo=timezone.utc)
    year_end = datetime(now.year + 1, 1, 1, tzinfo=timezone.utc)
    elapsed = (now - year_start).total_seconds()
    total = (year_end - year_start).total_seconds()
    return (elapsed / total) * 100

def progress_bar(percent):
    filled = math.floor((percent / 100) * BAR_LENGTH)
    return "█" * filled + "░" * (BAR_LENGTH - filled)

# ─── WEATHER ───────────────────────────────────────────────────────────────
def weather_code_to_text(code):
    mapping = {
        0: "clear sky",
        1: "mostly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "fog",
        48: "fog",
        51: "drizzle",
        61: "rain",
        71: "snow",
        80: "showers",
        95: "thunderstorms"
    }
    return mapping.get(code, "indecisive sky")

def get_madrid_weather():
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={MADRID_LAT}"
            f"&longitude={MADRID_LON}"
            "&daily=weathercode,temperature_2m_max,temperature_2m_min,"
            "apparent_temperature_max,sunrise,sunset"
            "&timezone=Europe/Madrid"
        )
        r = requests.get(url, timeout=10)
        d = r.json()["daily"]

        tmin = d["temperature_2m_min"][0]
        tmax = d["temperature_2m_max"][0]
        feels = d["apparent_temperature_max"][0]
        code = d["weathercode"][0]

        sunrise = datetime.fromisoformat(d["sunrise"][0])
        sunset = datetime.fromisoformat(d["sunset"][0])
        daylight_hours = (sunset - sunrise).total_seconds() / 3600

        return True, tmin, tmax, feels, weather_code_to_text(code), daylight_hours
    except Exception:
        return False, None, None, None, None, None

# ─── STATE ────────────────────────────────────────────────────────────────
def load_last_sent():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r") as f:
        return json.load(f).get("last_sent")

def save_last_sent(value):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_sent": value}, f)

# ─── MAIN ───────────────────────────────────────────────────────────────────
def main():
    now = datetime.now(timezone.utc)
    today_key = now.strftime("%Y-%m-%d")
    if load_last_sent() == today_key:
        return

    percent = year_progress_percentage()
    percent_str = f"{percent:.2f}"
    bar = progress_bar(percent)

    is_final_day = now.month == 12 and now.day == 31

    if is_final_day:
        quote = random.choice(FINAL_DAY_QUOTES)
        title = "📆 *Year completed*"
    elif percent < 35:
        quote = random.choice(EARLY_QUOTES)
        title = "📆 *Year progress update*"
    elif percent < 70:
        quote = random.choice(MID_QUOTES)
        title = "📆 *Year progress update*"
    else:
        quote = random.choice(LATE_QUOTES)
        title = "📆 *Year progress update*"

    emoji = random_emoji()

    ok, tmin, tmax, feels, condition, daylight = get_madrid_weather()

    if ok:
        weather_block = (
            f"\n🌍 *Madrid weather*\n"
            f"{tmin:.0f}°C – {tmax:.0f}°C, {condition} {random_emoji()}\n"
            f"Feels like {feels:.0f}°C. {random.choice(FEELS_LIKE_QUOTES)}\n"
            f"{daylight:.1f}h daylight. {random.choice(DAYLIGHT_QUOTES)}\n"
            f"_{random.choice(WEATHER_QUOTES)}_\n"
        )
    else:
        weather_block = (
            f"\n🌍 *Madrid weather*\n"
            f"Unavailable {random_emoji()}\n"
            f"_{random.choice(WEATHER_ERROR_QUOTES)}_\n"
            f"_{random.choice(DAYLIGHT_ERROR_QUOTES)}_\n"
        )

    message = (
        f"{title}\n\n"
        f"`{bar}`\n"
        f"*{percent_str}%* of the year is gone {emoji}\n"
        f"{weather_block}\n"
        f"_{quote}_"
    )

    send_message(message)
    save_last_sent(today_key)

if __name__ == "__main__":
    main()
