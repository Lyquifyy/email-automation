import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_summary(summary):
    msg = MIMEText(summary)
    msg["Subject"] = "Daily Email Summary"
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
