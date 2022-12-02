import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

import toml
from pydantic import BaseModel, ValidationError

from ..exceptions import ConfigurationError
from ..utils import backup_file


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
        home = Path().home()
        data = {
            'application': {'output_folder': str(home / 'parsed_general_ledgers'), },
            'parsers': {
                'sheet_name': 'General ledger',
                'start_row': 6,
                'column_mappings': {
                    '1': {'name': 'account_id', 'title': 'Account ID', 'width': 12},
                    '2': {'name': 'account_description', 'title': 'Account Description', 'width': 24},
                    '3': {'name': 'date', 'title': 'Date', 'number_format': 'DD/MM/YYYY', 'width': 12},
                    '4': {'name': 'reference', 'title': 'Reference', 'width': 30},
                    '5': {'name': 'journal', 'title': 'Jrnl', 'width': 12},
                    '6': {'name': 'description', 'title': 'Trans Description', 'width': 36},
                    '7': {'name': 'debit_amount', 'title': 'Debit Amt', 'number_format': '#,##0.00', 'width': 12},
                    '8': {'name': 'credit_amount', 'title': 'Credit Amt', 'number_format': '#,##0.00', 'width': 12},
                    '9': {'name': 'balance', 'title': 'Balance', 'number_format': '#,##0.00', 'width': 12},
                }}
        }
        return data

    def prep_config(self):
        raise Exception('Not implemented')

    def write_configuration(self, config_data: Dict[str, Any], over_write: bool = False, ) -> None:
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

    def get_configuration_obj(self) -> Any:
        raise Exception('Not implemented')

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
