from __future__ import print_function

from services.authentication import Authentication
from services.drive import Drive

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH =  './credentials/credentials.json'
TOKEN_PATH = './credentials/token.json' 


def main():
    drive_service, spred_service, gmail_service = Authentication(TOKEN_PATH, CREDENTIALS_PATH, SCOPES).get_services()

    drive = Drive(drive_service)
    drive.print_files()
    drive.print_folders()
    drive.copy_file_into('1KRuEbngTY9ok6mCOtCYsR6gMdSSHYSo2VfwddoakW_0', '14S-pQ_ea42ydP-4ejN6cYEDbwRe8wZn4')

if __name__ == '__main__':
    main()
