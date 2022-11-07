import os
from enum import Enum
from pathlib import Path
from typing import Dict, Any

import toml


class ConfigurationManager:

    def __init__(self, config_folder: Path = None):
        if config_folder is None:
            self.config_folder = Path().home() / '.py_cover_letters'
            self.config_folder.mkdir(exist_ok=True)
        self.config_file = self.config_folder / 'configuration.toml'
        self.username = os.getlogin()

    def get_sample_config(self):
        data = {'cover_letters': {'template_folder': str(self.config_folder / 'templates'),
                                  'default_template': 'Cover Letter Template.docx',
                                  'default_output_folder': str(Path(os.getcwd()) / 'output')},
                'gmail': {'email': f'{self.username}@gmail.com', 'token': 'SECRET'},
                'database': {'folder': str(Path(os.getcwd()) / 'data'), 'file': 'cover_letters.xlsx'}}
        return data

    def write_configuration(self, config_data: Dict[str, Any], over_write=False):
        if self.config_file.exists() and not over_write:
            raise Exception('Cannot overwrite config file.')
        with open(self.config_file, 'w') as f:
            toml.dump(config_data, f)

    def get_configuration(self):
        with open(self.config_file, 'r') as f:
            configuration = toml.load(f)
        return configuration

    @classmethod
    def get_current(cls):
        config = ConfigurationManager()
        return config.get_configuration()


def main(install: True):
    config_manager = ConfigurationManager()
    configuration = config_manager.get_sample_config()
    email = configuration['gmail']['email']
    new_email = input(f'Sender email <{email}>: ')
    if new_email != '':
        configuration['gmail']['email'] = new_email

    gmail_token = input('GMail token: ')
    configuration['gmail']['token'] = gmail_token
    print(configuration)
    config_manager.write_configuration(configuration, over_write=True)


if __name__ == '__main__':
    main(True)
