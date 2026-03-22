# 💊 WhatsApp Medicine Reminder Bot

A Python-based automation system that sends medicine reminders via WhatsApp using Twilio API.

---

## 🚀 Features

- 📲 WhatsApp-based interaction
- ⏰ Scheduled daily reminders
- 🔒 Secure credentials using environment variables
- ⚡ Real-time webhook integration using Flask
- 🧠 Input parsing with validation
- 🧵 Background scheduler using threading

---

## 🛠 Tech Stack

- Python
- Flask
- Twilio API
- Ngrok (for local tunneling)
- Schedule (task scheduler)

---

## 📦 Project Structure

```
Medicine_Reminder_Project/
│
├── app.py
├── requirements.txt
├── .env (not uploaded for security)
├── .gitignore
├── README.md
└── screenshots/
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/Medicine_Reminder_Project.git
cd Medicine_Reminder_Project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env` file
```
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
YOUR_PHONE=whatsapp:+91XXXXXXXXXX
```

### 4. Run the app
```bash
python app.py
```

### 5. Start ngrok
```bash
ngrok http 5000
```

### 6. Configure Twilio sandbox webhook
```
https://your-ngrok-url/whatsapp
```

---

## 📱 Usage

Send message on WhatsApp:

```
Crocin 14:30
```

You will receive:

```
Reminder set for Crocin at 14:30
```

---

## ⚠️ Limitations

- Works only with Twilio sandbox users
- Requires ngrok to stay active
- Single-user support (current version)

---

## 🔮 Future Improvements

- Multi-user support
- Database integration
- Prescription image upload (OCR)
- Cloud deployment
- Web dashboard

---
## 📸 Demo

![Demo](screenshots/demo.png)

## 👨‍💻 Author

Kaustubh Dubey  
B.Tech Automobile Engineering | Product Enthusiast

---

## ⭐ If you like this project, star the repo!