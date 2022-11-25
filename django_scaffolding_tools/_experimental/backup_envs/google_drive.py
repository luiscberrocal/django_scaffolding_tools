from pathlib import Path


def main():
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive

    secrets_file = Path(__file__).parent.parent.parent.parent / '.envs' / 'google_drive' / 'client_secrets.json'
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = str(secrets_file)
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    # gauth.CommandLineAuth()

    drive = GoogleDrive(gauth)

    # Auto-iterate through all files in the root folder.
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    for file1 in file_list:
        print('title: %s, id: %s kind: %s' % (file1['title'], file1['id'], file1['kind']))

if __name__ == '__main__':
    main()
