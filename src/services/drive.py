from googleapiclient.errors import HttpError
from datetime import datetime

class Drive:
    def __init__(self, service):
        self.service = service

    def copy_weekly_ata(self):
        ata_id = self.get_ata_id()

        folder_id = self.get_folder_id()

        today = datetime.now()
        currrent_date = today.strftime("%d/%m/%Y")

        self.copy_file_into(ata_id, folder_id, currrent_date )

        # print(f"ata id: {ata_id}")
        # print(f"folder id: {folder_id}")

    def get_folder_id(self):
        today = datetime.now()
        month_number = today.month

        folders = self.get_folders()

        def find_month_id(month):
            for folder in folders:
                if folder['name'] == month:
                    return folder['id']
            exit(f"cannot find folder for month: {month}")

        match month_number:
            case 1: return find_month_id('Janeiro') 
            case 2: return find_month_id('Fevereiro') 
            case 3: return find_month_id('Março') 
            case 4: return find_month_id('Abril') 
            case 5: return find_month_id('Maio') 
            case 6: return find_month_id('Junho') 
            case 7: return find_month_id('Julho') 
            case 8: return find_month_id('Agosto') 
            case 9: return find_month_id('Setembro') 
            case 10: return find_month_id('Outubro') 
            case 11: return find_month_id('Novembro') 
            case 12: return find_month_id('Dezembro') 
            case _:
                print("Invalid month number!")

    def copy_file_into(self, fileId, folderId, new_name):
        reqBody = {
            'parents': [ folderId ], 
            'name': new_name
        }

        try:
            result = self.service.files().copy(fileId=fileId, body=reqBody, fields='webViewLink').execute()
            print("File copied successfully!\n")
            link = result['webViewLink']
            print(f"Copied file link: {link}")
            return link
        except HttpError as error:
            print(f'An error occurred: {error}')

    def get_ata_id(self): 
        query = "'14S-pQ_ea42ydP-4ejN6cYEDbwRe8wZn4' in parents"
        try:
            results = self.service.files().list(pageSize=20, q=query).execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            for item in items:
                if item['name'] == 'Modelo Ata':
                    print(f"Ata found! => ${item['id']}")
                    return item['id']
            exit('Ata not found!')
        except HttpError as error:
            print(error)

    def get_folders(self):
        query = "mimeType = 'application/vnd.google-apps.folder' and '14S-pQ_ea42ydP-4ejN6cYEDbwRe8wZn4' in parents"
        try:
            results = self.service.files().list(pageSize=20, q=query).execute()
            folders = results.get('files', [])
            foldersDic  = []

            if not folders:
                print('No folders found.')
                return
            for folder in folders:
                foldersDic.append({'name': folder['name'], 'id': folder['id']})
            return folders

        except HttpError as error:
            print(error)
