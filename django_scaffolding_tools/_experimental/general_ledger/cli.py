import logging
import shutil
from datetime import datetime
from pathlib import Path

from django_scaffolding_tools._experimental.general_ledger.parsers import parse_general_ledger
from django_scaffolding_tools._experimental.general_ledger.writers import write_transactions


def separate_accounts(gl_file: Path, output_folder: Path, timestamp_format: str = '%Y%m%d_%H%M%S') -> Path:
    output_file = build_output_file(gl_file, output_folder, timestamp_format)
    shutil.copy(gl_file, output_file)
    transactions = parse_general_ledger(gl_file)

    write_transactions(output_file, transactions)
    return output_file


def clean_filename(filename: str):
    new_name = filename.replace('.', '').replace(',', '').replace(' ', '_')
    return new_name


def build_output_file(gl_file: Path, output_folder: Path, timestamp_format: str = '%Y%m%d_%H%M%S') -> Path:
    """Creates a filename based on the gl_file values in the output folder prepending a timestamp."""
    timestamp = datetime.now().strftime(timestamp_format)
    base_name = clean_filename(gl_file.stem)
    extention = gl_file.suffix
    output_file = output_folder / f'{timestamp}_{base_name}{extention}'
    return output_file


if __name__ == '__main__':
    outputfolder = Path(__file__).parent.parent.parent.parent / 'output'
    # glfile = outputfolder / 'ITA GL Export 2022 (1).xlsx'
    # rs = separate_accounts(glfile, outputfolder)
    # print(rs)

    log_file = outputfolder / 'exampel.log'
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')
    logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
