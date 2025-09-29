# send_once.py
import os
from twilio.rest import Client
from dotenv import load_dotenv

# load secrets from .env
load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
FROM = os.getenv("TWILIO_WHATSAPP_FROM")
TO = os.getenv("RECIPIENT")

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_=FROM,
    to=TO,
    body="Hello 👋 This is your test diet reminder from Twilio!"
)

print("Message sent! SID:", message.sid)
