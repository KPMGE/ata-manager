from __future__ import print_function

from services.authentication import Authentication
from services.drive import Drive

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets.readonly']
CREDENTIALS_PATH =  './src/credentials/credentials.json'
TOKEN_PATH = './src/credentials/token.json' 

SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

def main():
    drive_service, spred_service, gmail_service = Authentication(TOKEN_PATH, CREDENTIALS_PATH, SCOPES).get_services()

    drive = Drive(drive_service)
    drive.print_files()
    drive.print_folders()

if __name__ == '__main__':
    main()
