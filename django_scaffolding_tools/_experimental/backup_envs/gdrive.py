# import the required libraries
import json
import pickle
import os.path
from mimetypes import MimeTypes
from pathlib import Path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

from django_scaffolding_tools._experimental.backup_envs.exceptions import UploadError


class GDrive:
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self, secrets_file: Path):
        self.secrets_file = secrets_file
        token_file = secrets_file.parent / 'token.pickle'
        creds = self.get_g_drive_credentials(token_file)
        self.service = build('drive', 'v3', credentials=creds)

    def get_g_drive_credentials(self, token_file):
        creds = None
        # The file token.pickle stores the
        # user's access and refresh tokens. It is
        # created automatically when the authorization
        # flow completes for the first time.
        # Check if file token.pickle exists
        if token_file.exists():
            # Read the token from the file and
            # store it in the variable creds
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        # If no valid credentials are available,
        # request the user to log in.
        if not creds or not creds.valid:

            # If token is expired, it will be refreshed,
            # else, we will request a new one.
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(self.secrets_file), self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle
            # file for future usage
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def upload(self, file_to_upload: Path, folder_id: str):
        filename = file_to_upload.name
        mime_type = 'application/octet-stream'
        body = {'name': filename, 'parents': [folder_id], 'mimeType': mime_type}
        try:
            media_body = MediaFileUpload(file_to_upload, mimetype=mime_type, chunksize=10485760, resumable=True)
            request = self.service.files().create(body=body, media_body=media_body)  # Modified
            result = request.execute()
            return result
        except Exception as e:
            error_message = f'Upload error. Type {e.__class__.__name__} error {e}'
            raise UploadError(error_message)

    # Define the SCOPES. If modifying it,
    # delete the token.pickle file.


SCOPES = ['https://www.googleapis.com/auth/drive']


# Create a function get_file_list with
# parameter N which is the length of
# the list of files.


def get_file_list(N):
    g_drive_folder = Path(__file__).parent.parent.parent.parent / '.envs' / 'google_drive'
    secrets_file = g_drive_folder / 'client_secrets.json'
    token_file = g_drive_folder / 'token.pickle'
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = get_g_drive_credentials(secrets_file, token_file)

    # Connect to the API service
    service = build('drive', 'v3', credentials=creds)

    # request a list of first N files or
    # folders with name and id from the API.
    resource = service.files()
    result = resource.list(pageSize=N, fields="files(id, name)",
                           q="mimeType = 'application/vnd.google-apps.folder' and name = 'Envs'", ).execute()

    # return the result dictionary containing
    # the information about the files
    return result


def get_g_drive_credentials(secrets_file, token_file):
    creds = None
    # The file token.pickle stores the
    # user's access and refresh tokens. It is
    # created automatically when the authorization
    # flow completes for the first time.
    # Check if file token.pickle exists
    if token_file.exists():
        # Read the token from the file and
        # store it in the variable creds
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If no valid credentials are available,
    # request the user to log in.
    if not creds or not creds.valid:

        # If token is expired, it will be refreshed,
        # else, we will request a new one.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(secrets_file), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle
        # file for future usage
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def old_way():
    # Get list of first 5 files or
    # folders from our Google Drive Storage
    result_dict = get_file_list(150)

    # Extract the list from the dictionary
    file_list = result_dict.get('files')

    # Print every file's name
    print(f'Results {len(file_list)}')
    for file in file_list:
        if file['name'] == 'Envs':
            print(file['name'], file['id'])
        else:
            print('*', end='', flush=False)


def main():
    g_drive_folder = Path(__file__).parent.parent.parent.parent / '.envs' / 'google_drive'
    secrets_file = g_drive_folder / 'client_secrets.json'

    folder_ids_file = g_drive_folder / 'google_drive_folders_id.json'
    with open(folder_ids_file, 'r') as json_file:
        folder_ids = json.load(json_file)
    folder_id = folder_ids['Envs']

    gdrive = GDrive(secrets_file)
    test_file = Path(
        '/home/luiscberrocal/PycharmProjects/django_scaffolding_tools/.envs/google_drive/google_drive_folders_id.json')
    r = gdrive.upload(test_file, folder_id)
    assert r == ''

if __name__ == '__main__':
    main()
