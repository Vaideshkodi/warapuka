import os
import csv
from datetime import datetime, timedelta
import pytz
from twilio.rest import Client

# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp = os.getenv("TWILIO_WHATSAPP_FROM")
to_whatsapp = os.getenv("RECIPIENT")

client = Client(account_sid, auth_token)

# Read the CSV plan
plan = {}
with open("diet_plan.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        day = row["weekday"].strip()
        time = row["time"].strip()
        message = row["message"].strip()
        plan[(day, time)] = message

# Use JST timezone (change if you’re in IST or another zone)
tz = pytz.timezone("Asia/Tokyo")
now = datetime.now(tz)
weekday = now.strftime("%A")

# Create ±2 min window
times_to_check = [(now + timedelta(minutes=i)).strftime("%H:%M") for i in range(-2, 3)]

# Check if we have a message
msg = None
for t in times_to_check:
    key = (weekday, t)
    if key in plan:
        msg = plan[key]
        break

if not msg:
    msg = f"No message scheduled at this time ra puka. (Checked window: {times_to_check})"

# Send WhatsApp message
message = client.messages.create(
    body=msg,
    from_=from_whatsapp,
    to=to_whatsapp
)

print(f"Message sent: {msg}")
