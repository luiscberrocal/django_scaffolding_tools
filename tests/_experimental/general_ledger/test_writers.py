from django_scaffolding_tools._experimental.general_ledger.parsers import parse_general_ledger
from django_scaffolding_tools._experimental.general_ledger.writers import write_transactions


def test_parse_general_ledger(output_folder):
    gl_file = output_folder / 'ITA GL Export 2022 (1).xlsx'
    transactions = parse_general_ledger(gl_file)

    new_file = output_folder / 'transac2.xlsx'
    write_transactions(new_file, transactions)
