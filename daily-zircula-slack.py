{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww30040\viewh16340\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import requests\
from ics import Calendar\
from datetime import datetime\
import pytz\
\
# =========================\
# \uc0\u55357 \u56615  CONFIG (FERTIG)\
# =========================\
\
ICS_URLS = [\
    "https://nextcloud.zircula.org/remote.php/dav/public-calendars/2QANrakA3wBbyxmt?export",\
    "https://pretix.eu/werk/events/ical/?locale=de",\
    "https://easyverein.com/event/subscription/Zolli/20c60380-63bb-42ea-95cd-8b44358f3330/calendar.ics"\
]\
\
SLACK_WEBHOOK = "HIER_DEIN_NEUER_WEBHOOK"\
\
TIMEZONE = "Europe/Berlin"\
\
# =========================\
# SETUP\
# =========================\
\
tz = pytz.timezone(TIMEZONE)\
now = datetime.now(tz)\
today = now.date()\
\
events_today = []\
\
# =========================\
# EVENTS LADEN\
# =========================\
\
for url in ICS_URLS:\
    try:\
        response = requests.get(url, timeout=10)\
        cal = Calendar(response.text)\
\
        for event in cal.events:\
            if not event.begin:\
                continue\
\
            event_time = event.begin.to(TIMEZONE).datetime\
            event_date = event_time.date()\
\
            if event_date == today:\
                events_today.append(\{\
                    "name": event.name,\
                    "time": event_time.strftime("%H:%M"),\
                    "location": event.location or "",\
                    "url": event.url or ""\
                \})\
\
    except Exception as e:\
        print(f"Fehler bei \{url\}: \{e\}")\
\
# =========================\
# SORTIEREN + DUPLIKATE\
# =========================\
\
events_today.sort(key=lambda x: x["time"])\
\
seen = set()\
unique_events = []\
\
for e in events_today:\
    key = (e["name"], e["time"])\
    if key not in seen:\
        seen.add(key)\
        unique_events.append(e)\
\
# =========================\
# SLACK TEXT\
# =========================\
\
if unique_events:\
    text = "\uc0\u55357 \u56517  *Zircula \'96 Heute:*\\n\\n"\
\
    for e in unique_events:\
        text += f"\'95 *\{e['time']\}* \'96 \{e['name']\}\\n"\
\
        if e["location"]:\
            text += f"   \uc0\u55357 \u56525  \{e['location']\}\\n"\
\
        if e["url"]:\
            text += f"   \uc0\u55357 \u56599  \{e['url']\}\\n"\
\
else:\
    text = "\uc0\u55357 \u56517  *Zircula \'96 Heute:*\\n\\nKeine Termine \u55356 \u57225 "\
\
# =========================\
# SENDEN\
# =========================\
\
payload = \{"text": text\}\
\
requests.post(SLACK_WEBHOOK, json=payload)\
\
print("\uc0\u9989  Zircula Tages\'fcbersicht gesendet")}