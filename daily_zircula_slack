import requests
from ics import Calendar
from datetime import datetime
import pytz

# =========================
# 🔧 CONFIG (FERTIG)
# =========================

ICS_URLS = [
    "https://nextcloud.zircula.org/remote.php/dav/public-calendars/2QANrakA3wBbyxmt?export",
    "https://pretix.eu/werk/events/ical/?locale=de",
    "https://easyverein.com/event/subscription/Zolli/20c60380-63bb-42ea-95cd-8b44358f3330/calendar.ics"
]

SLACK_WEBHOOK = "https://hooks.slack.com/services/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"

TIMEZONE = "Europe/Berlin"

# =========================
# SETUP
# =========================

tz = pytz.timezone(TIMEZONE)
now = datetime.now(tz)
today = now.date()

events_today = []

# =========================
# EVENTS LADEN
# =========================

for url in ICS_URLS:
    try:
        response = requests.get(url, timeout=10)
        cal = Calendar(response.text)

        for event in cal.events:
            if not event.begin:
                continue

            event_time = event.begin.to(TIMEZONE).datetime
            event_date = event_time.date()

            if event_date == today:
                events_today.append({
                    "name": event.name,
                    "time": event_time.strftime("%H:%M"),
                    "location": event.location or "",
                    "url": event.url or ""
                })

    except Exception as e:
        print(f"Fehler bei {url}: {e}")

# =========================
# SORTIEREN + DUPLIKATE
# =========================

events_today.sort(key=lambda x: x["time"])

seen = set()
unique_events = []

for e in events_today:
    key = (e["name"], e["time"])
    if key not in seen:
        seen.add(key)
        unique_events.append(e)

# =========================
# SLACK TEXT
# =========================

if unique_events:
    text = "📅 *Zircula – Heute:*\n\n"

    for e in unique_events:
        text += f"• *{e['time']}* – {e['name']}\n"

        if e["location"]:
            text += f"   📍 {e['location']}\n"

        if e["url"]:
            text += f"   🔗 {e['url']}\n"

else:
    text = "📅 *Zircula – Heute:*\n\nKeine Termine 🎉"

# =========================
# SENDEN
# =========================

payload = {"text": text}

requests.post(SLACK_WEBHOOK, json=payload)

print("✅ Zircula Tagesübersicht gesendet")
