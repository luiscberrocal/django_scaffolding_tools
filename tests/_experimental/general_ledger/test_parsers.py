from django_scaffolding_tools._experimental.general_ledger.parsers import parse_general_ledger


def test_parse_general_ledger(output_folder):
    gl_file = output_folder / 'ITA GL Export 2022 (1).xlsx'
    trasactions = parse_general_ledger(gl_file)
    print(trasactions)
