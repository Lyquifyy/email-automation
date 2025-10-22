import requests
import json
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

def summarize_emails_ollama(emails):
    # Format emails neatly
    formatted_emails = ""
    for i, email in enumerate(emails, start=1):
        formatted_emails += f"""
Email {i}:
From: {email['sender']}
Date: {email['date']}
Subject: {email['subject']}
Body:
{email['body']}

---
"""

    prompt = f"""
You are a personal assistant summarizing emails from this week.

Summarize the following emails by grouping them by topic or sender.
Highlight any important updates, tasks, or follow-up items.
Be concise but specific.

Emails:
{formatted_emails}
"""

    # Send request to local Ollama model
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": True  # adjust as needed
        },
        stream=True,
    )

    summary = ""

    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                summary += data.get("response", "")
            except json.JSONDecodeError:
                continue # Skip any missconfigured lines.


    summary = summary.strip()

    print(summary)
    return summary
