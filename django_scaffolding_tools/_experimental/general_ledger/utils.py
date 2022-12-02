import shutil
from datetime import datetime
from pathlib import Path

from .exceptions import GLParserException


def backup_file(filename: Path, backup_folder: Path, add_version: bool = True) -> Path:
    if not backup_folder.is_dir():
        error_message = f'Backup folder has to be a folder.' \
                        f' Supplied: {backup_folder}. Type: {type(backup_folder)}'
        raise GLParserException(error_message)

    datetime_format = '%Y%m%d_%H%M%S'
    if add_version:
        from . import __version__ as current_version
        version_val = f'v{current_version}_'
    else:
        version_val = ''
    timestamp = datetime.datetime.now().strftime(datetime_format)
    backup_filename = backup_folder / f'{timestamp}_{version_val}{filename.name}'
    shutil.copy(filename, backup_filename)
    return backup_filename

