from googleapiclient.errors import HttpError
from datetime import datetime

MONTHS_PORTUGUESE = {
 1: 'Janeiro',
 2: 'Fevereiro',
 3: 'Março',
 4: 'Maio',
 5: 'Abril',
 6: 'Junho',
 7: 'Julho',
 8: 'Agosto',
 9: 'Setembro',
 10: 'Outubro',
 11: 'Novembro',
 12: 'Dezembro'
}

class Drive:
    def __init__(self, service):
        self.service = service

    def copy_weekly_ata(self, main_folder_id):
        today = datetime.now()
        currrent_date = today.strftime("%d/%m/%Y")

        save_file_folder_id = self.get_folders_inside(main_folder_id)[MONTHS_PORTUGUESE[today.month]]
        ata_id = self.get_ata_id(main_folder_id)

        self.copy_file_into(ata_id, save_file_folder_id , currrent_date)

    def copy_file_into(self, fileId, folderId, new_name):
        reqBody = { 'parents': [ folderId ], 'name': new_name }

        try:
            result = self.service.files().copy(fileId=fileId, body=reqBody, fields='webViewLink').execute()
            print("File copied successfully!\n")
            link = result['webViewLink']
            print(f"Copied file link: {link}")
            return link
        except HttpError as error:
            print(f'An error occurred: {error}')

    def get_ata_id(self, folder_id): 
        query = f"'{folder_id}' in parents"
        try:
            results = self.service.files().list(pageSize=20, q=query).execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            for item in items:
                if item['name'] == 'Modelo Ata':
                    print(f"Ata found!")
                    return item['id']
            exit('Ata not found!')
        except HttpError as error:
            print(error)

    def get_folders_inside(self, folder_id):
        query = f"mimeType = 'application/vnd.google-apps.folder' and '{folder_id}' in parents"
        try:
            results = self.service.files().list(pageSize=20, q=query).execute()
            folders = results.get('files', [])
            foldersDictionary = {}

            if not folders:
                print('No folders found.')
                return
            for folder in folders:
                foldersDictionary[folder['name']] = folder['id']
            return foldersDictionary

        except HttpError as error:
            print(error)
