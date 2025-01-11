import os
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple


def print_success(message):
    print(f"\033[92m {message}\033[00m")


def print_warning(message):
    print(f"\033[93m {message}\033[00m")


def print_error(message):
    print(f"\033[91m {message}\033[00m")


def list_all_projects(project_folder: Path) -> List[str]:
    folders = [x.path for x in os.scandir(project_folder) if x.is_dir()]
    return folders


def get_projects_envs(project_folder: Path) -> Dict[str, Any]:
    folders = list_all_projects(project_folder)
    folder_dict = dict()
    for folder in folders:
        path = Path(folder)
        envs = path / ".envs"
        if envs.exists():
            folder_dict[path.name] = {"envs": envs}
    return folder_dict


def zip_folder(zip_file: Path, folder_to_zip: Path):
    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(
                    os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, ".."))
                )

    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipdir(folder_to_zip, zipf)


def backup_envs(project_folder: Path, backup_folder: Path, date_format="%Y%m%d_%H") -> Tuple[List[Path], Path]:
    project_envs_dict = get_projects_envs(project_folder)
    timestamp = datetime.now().strftime(date_format)
    b_folder = backup_folder / timestamp
    b_folder.mkdir(exist_ok=True)
    zip_list = list()
    for project, v in project_envs_dict.items():
        zip_file = b_folder / f"{project}.zip"
        zip_folder(zip_file, v["envs"])
        zip_list.append(zip_file)
    return zip_list, b_folder


if __name__ == "__main__":
    home = Path().home()
    # project_folder_name = 'adelantos'
    project_folder_name = "PycharmProjects"
    m_folder = home / project_folder_name

    if not m_folder.exists():
        print(f"Folder {m_folder} does not exists")
        sys.exit(100)

    output_folder = home / "Documents" / f"{project_folder_name}_envs"
    output_folder.mkdir(exist_ok=True)

    zip_files, ts_backup_folder = backup_envs(m_folder, output_folder)
    for i, zf in enumerate(zip_files, 1):
        print_success(f"{i} {zf.name}")
    print_success(f"Wrote {len(zip_files)} zip files")
    print_success(f"Output folder: {ts_backup_folder}")
