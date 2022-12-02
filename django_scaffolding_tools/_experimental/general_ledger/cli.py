import shutil
from datetime import datetime
from pathlib import Path

from .parsers import parse_general_ledger
from .writers import write_transactions


def separate_accounts(gl_file: Path, output_folder: Path, timestamp_format: str = '%Y%m%d_%H%M%S') -> Path:
    output_file = build_output_file(gl_file, output_folder, timestamp_format)
    shutil.copy(gl_file, output_file)
    transactions = parse_general_ledger(gl_file)

    write_transactions(output_file, transactions)
    return output_file


def build_output_file(gl_file: Path, output_folder: Path, timestamp_format: str = '%Y%m%d_%H%M%S') -> Path:
    """Creates a filename based on the gl_file values in the output folder prepending a timestamp."""
    timestamp = datetime.now().strftime(timestamp_format)
    base_name = gl_file.name.replace(' ', '_')
    output_file = output_folder / f'{timestamp}_{base_name}'
    return output_file


if __name__ == '__main__':
    outputfolder = Path(__file__).parent.parent.parent.parent / 'output'
    glfile = outputfolder / 'ITA GL Export 2022 (1).xlsx'
    rs = separate_accounts(glfile, outputfolder)
    print(rs)
