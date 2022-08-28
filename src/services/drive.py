from googleapiclient.errors import HttpError

class Drive:
    def __init__(self, service):
        self.service = service

    def copy_file_into(self, fileId, folderId):
        reqBody = {'parents': [ folderId ]}

        try:
            self.service.files().copy(fileId=fileId, body=reqBody).execute()
            print("File copied successfully!\n")
        except HttpError as error:
            print(f'An error occurred: {error}')


    def print_folders(self):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=20,
            q="mimeType = 'application/vnd.google-apps.folder'"
        ).execute()

        items = results.get('files', [])

        if not items:
            print('No folders found.')
            return
        print('Folders:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

    def print_files(self):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=20,
        ).execute()

        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
