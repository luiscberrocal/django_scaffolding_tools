import logging
from pathlib import Path

from django_scaffolding_tools._experimental.reqs_utilities.parsers import parse_requirement_file, RequirementDatabase

logger = logging.getLogger(__name__)


class Updater:

    def __init__(self, database: RequirementDatabase):
        self.database = database

    def update_requirements(self, requirement_file: Path):
        reqs = parse_requirement_file(requirement_file)
        lines = list()
        logger.debug(f'Ready to parse {len(reqs)} requirement.')
        for req in reqs:
            if req['parsed'] is None:
                lines.append(req['raw'])
            else:
                recommended = self.database.get(req['parsed']['lib_name'])
                if recommended is None:
                    lines.append(req['raw'])
                else:
                    line = recommended.to_req_line()
                    lines.append(f'{line}\n')

        with open(requirement_file, 'w') as r_file:
            string_lines = ''.join(lines)
            r_file.write(string_lines)


if __name__ == '__main__':
    home = Path().home()
    db_file = home / 'PycharmProjects/django_scaffolding_tools/tests/fixtures/_experimental/req_db.json'
    db = RequirementDatabase(db_file)
    output_folder = Path(__file__).parent.parent.parent.parent / 'output'
    project = 'adelantos-cupos'
    project = 'ec-d-local-payment-collector'
    project = 'payment_router'
    update_requirements = False
    if update_requirements:
        files = ['local.txt', 'base.txt', 'production.txt']
        for file in files:
            f = home / f'adelantos/{project}/requirements/{file}'
            updater = Updater(db)
            updater.update_requirements(f)
    else:
        libraries = ['pytz', 'redis', 'hiredis']
        for lib in libraries:
            old_req = db.get(lib)
            req = db.update(lib)
            print(f'Old: {old_req}')
            print(f'New: {req}')
