# scheduler.py
import os
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

# load secrets
load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
FROM = os.getenv("TWILIO_WHATSAPP_FROM")
TO = os.getenv("RECIPIENT")

client = Client(account_sid, auth_token)

# 7-day diet messages (replace with your own full plan)
weekly = {
    "monday":    "🍎 Monday: Breakfast – Oats & milk; Lunch – 2 chapatis + dal; Dinner – paneer + veggies.",
    "tuesday":   "🥗 Tuesday: Breakfast – Poha; Lunch – Rice + dal + salad; Dinner – tofu stir-fry.",
    "wednesday": "🥬 Wednesday: Breakfast – Upma; Lunch – chapati + chole; Dinner – palak paneer.",
    "thursday":  "🍛 Thursday: Breakfast – Idli + chutney; Lunch – sambhar rice; Dinner – veg pulao.",
    "friday":    "🥕 Friday: Breakfast – Besan chilla; Lunch – dal + chapati; Dinner – veg khichdi.",
    "saturday":  "🙏 Saturday fast: Skip morning food. After sunset, vegetarian dinner – sabzi + chapati.",
    "sunday":    "🍉 Sunday: Breakfast – Fruit bowl; Lunch – rajma chawal; Dinner – paneer tikka + salad.",
}

def send_daily():
    today = datetime.now().strftime("%A").lower()  # e.g. "monday"
    text = weekly.get(today, "Here is your diet reminder.")
    msg = client.messages.create(from_=FROM, to=TO, body=text)
    print(f"Sent {today} message:", msg.sid)

# Scheduler
scheduler = BlockingScheduler(timezone="Asia/Tokyo")
scheduler.add_job(send_daily, "cron", hour=7, minute=30)  # 07:30 AM Tokyo time
print("Scheduler started... Waiting for daily messages.")
scheduler.start()
