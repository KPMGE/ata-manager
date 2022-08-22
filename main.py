# TODO: Make move file work
# TODO: Clean this code up
# TODO: Check if it's possible to copy a file into a folder automatically.

from __future__ import print_function
from drive import Drive
from googleapiclient.errors import HttpError

# let parentID = 'root'
# gapi.client.drive.files.list({
#   'q': `'${parentID}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false`,
#   'pageSize': 10,
#   'fields': "nextPageToken, files(id, name)"
# }).then(function(response) { do something with response })

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def move_file(service, fileId, parentFolderId):
    try:
        res = service.files().update(
            fileId=fileId,
            addParents=parentFolderId
        ).execute()

        print(res)
    except HttpError as error:
        print(f'An error occurred: {error}')

def copy_file(service, fileId):
    try:
        service.files().copy(fileId=fileId).execute()
        print("File copied!\n")
    except HttpError as error:
        print(f'An error occurred: {error}')

def main():
    drive = Drive('token.json', 'credentials.json', SCOPES)
    service = drive.getService()

    results = service.files().list(
        pageSize=20,
        q="mimeType = 'application/vnd.google-apps.folder'"
    ).execute()

    i2 = results.get('kind')
    for i in i2: 
        print(f'i = {i}')

    items = results.get('files', [])

    if not items:
        print('No files found.')
        return
    print('Contents:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()
