import os
import zipfile
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


if __name__ == '__main__':
    m_folder = Path('/home/luiscberrocal/adelantos')
    fs = get_projects_envs(m_folder)
    # for k, v in fs.items():
    #     print(f'{k} {v}')

    zf = Path('/home/luiscberrocal/PycharmProjects/django_scaffolding_tools/output/gt_payment_collector.zip')
    f2z = Path('/home/luiscberrocal/adelantos/gt_payment_collector/.envs')
    zip_folder(zf, f2z)
