from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path

class Authentication:
    def __init__(self, tokenPath, credentialsPath, scopes):
        self.tokenPath = tokenPath
        self.scopes = scopes
        self.credentialsPath = credentialsPath

    def get_services(self):
        creds = None
        if os.path.exists(self.tokenPath):
            creds = Credentials.from_authorized_user_file(self.tokenPath, self.scopes)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            print('not creds')
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentialsPath, self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.tokenPath, 'w') as token:
                token.write(creds.to_json())

        try:
            drive_service  = build('drive', 'v3', credentials=creds)
            spread_service = build('sheets', 'v4', credentials=creds)
            gmail_service  = build('gmail', 'v1', credentials=creds)
            return drive_service, spread_service, gmail_service
        except HttpError as error:
            print(f'An error occurred: {error}')
