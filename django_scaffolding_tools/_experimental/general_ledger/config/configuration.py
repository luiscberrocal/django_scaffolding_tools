import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

import toml
from pydantic import BaseModel, ValidationError

from ..exceptions import ConfigurationError
from ..utils import backup_file


class CoverLetter(BaseModel):
    template_folder: str
    default_template: str
    default_output_folder: str
    is_sample: Optional[bool] = True


class Gmail(BaseModel):
    email: str
    token: str


class Database(BaseModel):
    folder: str
    file: str
    backup_folder: str


class Configuration(BaseModel):
    cover_letters: CoverLetter
    gmail: Gmail
    database: Database


class ConfigurationManager:
    DEFAULT_CONFIG_FOLDER_NAME = '.py_gl_parser'
    DEFAULT_CONFIG_FILENAME = 'configuration.toml'

    def __init__(self, config_folder: Optional[Path] = None,
                 config_filename: Optional[str] = None):
        if config_folder is None:
            self.config_folder = Path().home() / self.DEFAULT_CONFIG_FOLDER_NAME
            self.config_folder.mkdir(exist_ok=True)
        else:
            self.config_folder = config_folder
        if config_filename is None:
            self.config_file = self.config_folder / self.DEFAULT_CONFIG_FILENAME
        else:
            self.config_file = self.config_folder / config_filename

        self.config_backup_folder = self.config_folder / 'backups'
        self.config_backup_folder.mkdir(exist_ok=True)

        self.username = os.getlogin()

        if not self.config_file.exists():
            tmp_config = self.get_sample_config()
            self.write_configuration(tmp_config)

    def get_sample_config(self) -> Dict[str, Any]:
        data = {'cover_letters': {'template_folder': str(self.config_folder / 'templates'),
                                  'default_template': 'Cover Letter Template.docx',
                                  'default_output_folder': str(Path(os.getcwd()) / 'output'),
                                  'is_sample': True},
                'gmail': {'email': f'{self.username}@gmail.com',
                          'token': 'SECRET'},
                'database': {'folder': str(Path(os.getcwd()) / 'data'),
                             'file': 'cover_letters.xlsx',
                             'backup_folder': str(Path(os.getcwd()) / 'data' / 'backups')}
                }
        return data

    def prep_config(self):
        config = self.get_configuration_obj()
        folder = Path(config.database.folder)
        folder.mkdir(exist_ok=True)
        folder = Path(config.database.backup_folder)
        folder.mkdir(exist_ok=True)

    def write_configuration(self, config_data: Dict[str, Any], over_write: bool = False,
                            is_sample: bool=False) -> None:
        if self.config_file.exists() and not over_write:
            raise Exception('Cannot overwrite config file.')
        with open(self.config_file, 'w') as f:
            toml.dump(config_data, f)

    def get_configuration(self) -> Dict[str, Any]:
        if not self.config_folder.exists():
            error_message = 'No configuration file found. Run py-cover-letters config.'
            raise ConfigurationError(error_message)

        with open(self.config_file, 'r') as f:
            configuration = toml.load(f)
        return configuration

    def get_configuration_obj(self) -> Configuration:
        config = self.get_configuration()
        config_obj = Configuration(**config)
        return config_obj

    def export_to_json(self, export_file: Path) -> None:
        config = self.get_configuration()
        with open(export_file, 'w') as f:
            json.dump(config, f)

    def is_valid(self, raise_error: bool = False) -> bool:
        try:
            self.get_configuration_obj()
            return True
        except ValidationError as e:
            error_msg = f'Configuration error. Type: {e.__class__.__name__} Error: {e}'
            if raise_error:
                raise ConfigurationError(error_msg)
            return False

    def backup(self) -> Path:
        backup_filename = backup_file(self.config_file, self.config_backup_folder)
        return backup_filename

    def delete(self) -> Path:
        backup_file = self.backup()
        self.config_file.unlink(missing_ok=True)
        return backup_file

    @classmethod
    def get_current(cls):
        config = cls()
        return config.get_configuration()
