from pathlib import Path


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
    secrets_file = Path(__file__).parent.parent.parent.parent / '.envs' / 'google_drive' / 'client_secrets.json'
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = str(secrets_file)
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    # gauth.CommandLineAuth()
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


if __name__ == '__main__':
    # main()

    gd_ifd = ''  # get form google_drive_folder_id.json
    z_folder = Path('/home/luiscberrocal/Documents/adelantos_envs/20221221_10')
    upload(z_folder, gd_ifd)
