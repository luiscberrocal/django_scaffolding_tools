import os
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


def list_all_projects(project_folder: Path) -> List[str]:
    folders = [x.path for x in os.scandir(project_folder) if x.is_dir()]
    return folders


def get_projects_envs(project_folder: Path) -> Dict[str, Any]:
    folders = list_all_projects(project_folder)
    folder_dict = dict()
    for folder in folders:
        path = Path(folder)
        envs = path / '.envs'
        if envs.exists():
            folder_dict[path.name] = {'envs': envs}
    return folder_dict


def zip_folder(zip_file: Path, folder_to_zip: Path):
    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                                           os.path.join(path, '..')))

    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(folder_to_zip, zipf)


def backup_envs(project_folder: Path, backup_folder: Path) -> List[Path]:
    project_envs_dict = get_projects_envs(project_folder)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    b_folder = backup_folder / timestamp
    b_folder.mkdir(exist_ok=True)
    zip_list = list()
    for project, v in project_envs_dict.items():
        zip_file = b_folder / f'{project}.zip'
        zip_folder(zip_file, v['envs'])
        zip_list.append(zip_file)
    return zip_list


if __name__ == '__main__':
    home = Path().home()
    m_folder = home / 'adelantos'
    output_folder = home / 'Documents' / 'adelantos_envs'

    zip_files = backup_envs(m_folder, output_folder)
    for i, zf in enumerate(zip_files, 1):
        print(f'{i} {zf.name}')
