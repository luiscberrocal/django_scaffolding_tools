from django_scaffolding_tools._experimental.general_ledger.parsers import parse_general_ledger

import logging


def test_parse_general_ledger(output_folder):
    gl_file = output_folder / 'ITA GL Export 2022 (1).xlsx'
    trasactions = parse_general_ledger(gl_file)
    print(trasactions)


def test_logging(output_folder):
    log_file = output_folder / 'exampel.log'
    logging.basicConfig(filename=log_file.root, encoding='utf-8', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')
    logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
