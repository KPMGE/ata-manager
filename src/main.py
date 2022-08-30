from services.authentication import Authentication
from services.drive import Drive
from services.spreadsheet import Spreadsheet
from services.email import send_emails

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_PATH =  './credentials/credentials.json'
TOKEN_PATH = './credentials/token.json' 

SPREADSHEET_ID = 'sheetID'
RANGE = "!A1:E14"

ATA_MAIN_FOLDER_ID = 'folderID'
SENDER_MAIL = 'sender@gmail.com'

def main():
    #Deverá rodar temporariamente
    drive_service, spread_service = Authentication(TOKEN_PATH, CREDENTIALS_PATH, SCOPES).get_services()

    drive = Drive(drive_service)
    ata_link = drive.copy_weekly_ata(ATA_MAIN_FOLDER_ID)

    spreadsheet = Spreadsheet(spread_service, SPREADSHEET_ID, RANGE)
    students = spreadsheet.get_students()

    spreadsheet.get_time()
    writer_name = spreadsheet.get_todays_writer()
    print(f"o aluno responsável pela ATA é {writer_name}")

    send_emails(students, writer_name, ata_link, SENDER_MAIL)

if __name__ == '__main__':
    main()
