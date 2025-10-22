from email_reader import get_emails  # from earlier Gmail API step
from summarizer import summarize_emails_ollama
from sender import send_summary
from model import start_ollama_model
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

if __name__ == "__main__":
    modelProcess = start_ollama_model(OLLAMA_MODEL)
    emails = get_emails()
    summary = summarize_emails_ollama(emails)
    send_summary(summary)
    modelProcess.terminate()
