import os
import csv
import pytz
from datetime import datetime
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

# Current weekday and time
now = datetime.now(pytz.timezone("Asia/Tokyo"))
weekday = now.strftime("%A")   # e.g. "Monday"
time_str = now.strftime("%H:%M")

# Check if we have a message
key = (weekday, time_str)
if key in plan:
    msg = plan[key]
    message = client.messages.create(
        body=msg,
        from_=from_whatsapp,
        to=to_whatsapp
    )
    print(f"Message sent: {msg}")
else:
    message = client.messages.create(
        body="No message at this time ra lovede",
        from_=from_whatsapp,
        to=to_whatsapp
    )
    print("No message scheduled at this time.")
    
