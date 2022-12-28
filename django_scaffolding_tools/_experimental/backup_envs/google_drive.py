import json
import os
import pickle
from pathlib import Path

from django_scaffolding_tools._experimental.backup_envs.gdrive import get_g_drive_credentials


def main():
    drive = get_google_drive()

    # Auto-iterate through all files in the root folder.
    folder = 'root'
    file_list = drive.ListFile({'q': f"'{folder}' in parents and trashed=false"}).GetList()

    for file1 in file_list:
        print('title: %s, id: %s kind: %s' % (file1['title'], file1['id'], file1['kind']))


def get_google_drive():
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive

    secrets_folder = Path(__file__).parent.parent.parent.parent / '.envs' / 'google_drive'
    secrets_file = secrets_folder / 'client_secrets.json'
    token_file = secrets_folder / 'token2.json'

    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = str(secrets_file)
    gauth = GoogleAuth()
    if token_file.exists():
        gauth.LoadCredentialsFile(token_file)
    else:
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile(token_file)

    drive = GoogleDrive(gauth)
    return drive


def upload(folder: Path, google_drive_folder: str):
    drive = get_google_drive()
    zip_files = folder.glob('**/*.zip')
    for i, zip_file in enumerate(zip_files, 1):
        print(f'{i} {zip_file}')
        gfile = drive.CreateFile({'parents': [{'id': google_drive_folder}]})
        # Read file and set it as the content of this instance.
        gfile.SetContentFile(str(zip_file))
        gfile.Upload()  # Upload the file.


def list_directories(folder: Path, top: int = 3):
    env_folders = list()
    for root, dirs, files in os.walk(folder):
        dirs.reverse()
        filtered = dirs[:top]
        for directory in filtered:
            env_folders.append(directory)
            print(directory)
    return env_folders


if __name__ == '__main__':
    # main()

    g_drive_folder = Path(__file__).parent.parent.parent.parent / '.envs' / 'google_drive'
    folder_ids_file = g_drive_folder / 'google_drive_folders_id.json'
    with open(folder_ids_file, 'r') as json_file:
        folder_ids = json.load(json_file)
    folder_id = folder_ids['Envs']

    envs_folder = Path('/home/luiscberrocal/Documents/adelantos_envs')

    last_folder = list_directories(envs_folder, top=1)[0]

    z_folder = envs_folder / last_folder
    prompt = input(f'Upload {last_folder} to gdrive? ')
    if prompt.lower() == 'y':
        upload(z_folder, folder_id)
