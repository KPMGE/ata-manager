from __future__ import print_function

from services.authentication import Authentication
from services.drive import Drive
# from services.spreadsheet import Spreadsheet

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_PATH =  './credentials/credentials.json'
TOKEN_PATH = './credentials/token.json' 

SPREADSHEET_ID = '1KRAJjUC3ysqL0r_g-iDO63Eijd5Ji-4yYGQvjdNtBhA'
RANGE = "!A1:E14"

def main():

    #Deverá rodar temporariamente

    drive_service, spread_service, gmail_service = Authentication(TOKEN_PATH, CREDENTIALS_PATH, SCOPES).get_services()

    drive = Drive(drive_service)
    drive.copy_weekly_ata()
    # drive.get_folders()
    # drive.print_files()

    # spreadsheet = Spreadsheet(spread_service, SPREADSHEET_ID, RANGE)
    # spreadsheet.get_emails()
    # spreadsheet.get_time()
    # name,email = spreadsheet.get_todays_writer()
    # print(f"o aluno responsável pela ATA é {name}")
    # print(f"email: {email}")

if __name__ == '__main__':
    main()
