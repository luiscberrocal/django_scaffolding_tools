import shutil
from datetime import datetime
from pathlib import Path

from django_scaffolding_tools._experimental.general_ledger.parsers import parse_general_ledger
from django_scaffolding_tools._experimental.general_ledger.writers import write_transactions


def separate_accounts(gl_file: Path, output_folder: Path, timestamp_format:str = '%Y%m%d_%H%M%S'):
    timestamp = datetime.now().strftime(timestamp_format)
    base_name = gl_file.name.replace(' ', '_')
    output_file = output_folder / f'{timestamp}_{base_name}'
    shutil.copy(gl_file, output_file)
    transactions = parse_general_ledger(gl_file)

    write_transactions(output_file, transactions)
    return output_file



if __name__ == '__main__':
    outputfolder = Path(__file__).parent.parent.parent.parent / 'output'
    glfile = outputfolder / 'ITA GL Export 2022 (1).xlsx'
    rs = separate_accounts(glfile, outputfolder)
    print(rs)
