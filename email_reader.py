from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os
import re
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

TOKEN_PATH = os.getenv("TOKEN_PATH")
SCOPES = [os.getenv("SCOPES")]
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")

def clean_text(text):
    """Remove invisible/unicode junk and normalize spaces."""
    text = re.sub(r'[\u200c\u200b\ufeff]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_emails():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Get last 7 days
    date_since = (datetime.now() - timedelta(days=7)).strftime("%Y/%m/%d")
    query = f"after:{date_since}"

    results = service.users().messages().list(userId='me', q=query, maxResults=50).execute()
    messages = results.get('messages', [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        
        headers = msg_data['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
        internal_date = int(msg_data.get('internalDate', 0)) / 1000
        date_str = datetime.fromtimestamp(internal_date).strftime("%Y-%m-%d %H:%M:%S")

        # Try to extract plain text body
        parts = msg_data['payload'].get('parts', [])
        body = ""
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    import base64
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    break

        if not body:
            body = msg_data.get('snippet', '')

        body = clean_text(body)

        emails.append({
            "date": date_str,
            "sender": sender,
            "subject": subject,
            "body": body
        })

    return emails

