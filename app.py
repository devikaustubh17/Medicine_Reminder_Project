from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import schedule
import time
import threading
import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Twilio credentials (from environment)
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)

from_whatsapp = os.getenv("TWILIO_WHATSAPP_NUMBER")

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("reminders.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT,
    medicine TEXT,
    time TEXT
)
""")
conn.commit()

# ---------------- SEND MESSAGE ----------------
def send_whatsapp(to_number, message):
    try:
        client.messages.create(
            body=message,
            from_=from_whatsapp,
            to=to_number
        )
        print(f"✅ Sent to {to_number}: {message}")
    except Exception as e:
        print("❌ Error sending message:", e)

# ---------------- SCHEDULER JOB ----------------
def job(phone, medicine):
    send_whatsapp(phone, f"💊 Reminder: Take {medicine}")

# ---------------- WEBHOOK ----------------
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From')

    print("📩 From:", from_number)
    print("📩 Message:", incoming_msg)

    resp = MessagingResponse()

    # -------- HELP MESSAGE --------
    if incoming_msg.lower() == "hi":
        resp.message(
            "👋 Welcome to Medicine Reminder Bot!\n\n"
            "Send in format:\n"
            "Paracetamol 21:45\n\n"
            "I will remind you daily 💊"
        )
        return str(resp)

    # -------- VIEW REMINDERS --------
    if incoming_msg.lower() == "my reminders":
        cursor.execute("SELECT medicine, time FROM reminders WHERE phone=?", (from_number,))
        rows = cursor.fetchall()

        if not rows:
            resp.message("❌ No reminders found")
        else:
            message = "📋 Your reminders:\n"
            for r in rows:
                message += f"{r[0]} at {r[1]}\n"
            resp.message(message)

        return str(resp)

    # -------- DELETE REMINDER --------
    if incoming_msg.lower().startswith("delete"):
        try:
            medicine = incoming_msg.split(" ")[1]

            cursor.execute(
                "DELETE FROM reminders WHERE phone=? AND medicine=?",
                (from_number, medicine)
            )
            conn.commit()

            resp.message(f"🗑 Deleted reminder for {medicine}")
        except:
            resp.message("❌ Use format: delete MedicineName")

        return str(resp)

    # -------- ADD REMINDER --------
    try:
        parts = incoming_msg.split()
        medicine = parts[0]
        time_input = parts[1]

        # Save in DB
        cursor.execute(
            "INSERT INTO reminders (phone, medicine, time) VALUES (?, ?, ?)",
            (from_number, medicine, time_input)
        )
        conn.commit()

        # Schedule job
        schedule.every().day.at(time_input).do(job, from_number, medicine)

        resp.message(f"✅ Reminder set for {medicine} at {time_input}")

    except:
        resp.message("❌ Format: MedicineName HH:MM")

    return str(resp)

# ---------------- RUN SCHEDULER ----------------
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler, daemon=True).start()

# ---------------- ROOT CHECK (FOR RENDER) ----------------
@app.route("/")
def home():
    return "✅ Medicine Reminder Bot is running!"

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)