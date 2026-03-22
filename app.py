from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import schedule
import time
import threading
import os
from dotenv import load_dotenv

# ---------------- INITIAL SETUP ----------------
load_dotenv()
app = Flask(__name__)

# Load credentials securely
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP = os.getenv("TWILIO_WHATSAPP_NUMBER")
TO_WHATSAPP = os.getenv("YOUR_PHONE")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Store reminders (in-memory for now)
reminders = []

# ---------------- SEND MESSAGE ----------------
def send_whatsapp(message):
    try:
        client.messages.create(
            body=message,
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP
        )
        print(f"[SUCCESS] Sent: {message}")
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")

# ---------------- PARSE INPUT ----------------
def parse_message(msg):
    try:
        parts = msg.split(" ")
        medicine = " ".join(parts[:-1])
        time_input = parts[-1]

        # Basic validation
        if ":" not in time_input:
            raise ValueError("Invalid time format")

        return medicine, time_input
    except:
        return None, None

# ---------------- WHATSAPP WEBHOOK ----------------
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body").strip()
    print(f"[INCOMING] {incoming_msg}")

    resp = MessagingResponse()

    medicine, time_input = parse_message(incoming_msg)

    if not medicine or not time_input:
        resp.message("❌ Format: MedicineName HH:MM (24-hour format)")
        return str(resp)

    def job():
        send_whatsapp(f"💊 Reminder: Take {medicine}")

    schedule.every().day.at(time_input).do(job)

    reminders.append({
        "medicine": medicine,
        "time": time_input
    })

    resp.message(f"✅ Reminder set for {medicine} at {time_input}")
    return str(resp)

# ---------------- STATUS ROUTE ----------------
@app.route("/")
def home():
    return "✅ Medicine Reminder Bot is running!"

# ---------------- SCHEDULER ----------------
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler, daemon=True).start()

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(port=5000)