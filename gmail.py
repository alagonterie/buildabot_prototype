import base64
import os
from email.mime.text import MIMEText
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient import errors

gmail_service = None
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


def send_log(message_text, subject):
    global gmail_service
    if gmail_service is None:
        gmail_service = get_auth_gmail_service()

    mime = MIMEText(message_text)
    user_profile = gmail_service.users().getProfile(userId='me').execute()
    mime['to'] = user_profile['emailAddress']
    mime['subject'] = subject
    email = {'raw': base64.urlsafe_b64encode(mime.as_string().encode()).decode()}

    try:
        sent_message = gmail_service.users().messages().send(userId='me', body=email).execute()
        return sent_message
    except errors.HttpError as error:
        print(f'A gmail error occurred: {error}')


def get_auth_gmail_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service
