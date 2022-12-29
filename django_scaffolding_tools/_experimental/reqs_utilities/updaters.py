import json
from pathlib import Path

from django_scaffolding_tools._experimental.reqs_utilities.parsers import parse_requirement_file


class Updater:

    def __init__(self, permitted_json_file: Path):
        with open(permitted_json_file, 'r') as j_file:
            self.permitted_libs = json.load(j_file)

    def update_requirements(self, requirement_file: Path):
        reqs = parse_requirement_file(requirement_file)
        lines = list()
        for req in reqs:
            if req['parsed'] is None:
                lines.append(req['raw'])
            elif self.permitted_libs.get(req['parsed']['lib_name']) is not None:
                line = f'{req["parsed"]["lib_name"]}=={self.permitted_libs.get(req["parsed"]["lib_name"])}\n'
                lines.append(line)
            else:
                lines.append(req['raw'])

        with open(requirement_file, 'w') as r_file:
            string_lines = ''.join(lines)
            r_file.write(string_lines)


if __name__ == '__main__':
    output_folder = Path(__file__).parent.parent.parent.parent / 'output'
    f = Path('/home/luiscberrocal/adelantos/adelantos-cupos/requirements/local.txt')

    permitted_versions = output_folder / 'permitted.json'

    updater = Updater(permitted_json_file=permitted_versions)
    updater.update_requirements(f)
