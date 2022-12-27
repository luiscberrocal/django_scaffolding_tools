# import the required libraries
import pickle
import os.path
from pathlib import Path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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
