import json
import os
import re
from pathlib import Path
from typing import Dict

from johnnydep.pipper import get_versions

from django_scaffolding_tools._experimental.reqs_utilities.models import RecommendedRequirement


def parse_for_permitted_libs(req_file: Path):
    regexp = re.compile(r'(?P<lib_name>[\w_\-]+)==(?P<version>[\w\.\-]+)\s*#?(?P<comment>.*)')
    with open(req_file, 'r') as r_file:
        lines = r_file.readlines()
    parsed_requirements = dict()
    for i, line in enumerate(lines, 1):
        match = regexp.match(line)
        if match:
            lib_name = match.group('lib_name')
            parsed_requirements[lib_name] = match.group('version')
    return parsed_requirements


class RequirementDatabase:

    def __init__(self, source_file: Path):
        self.source_file = source_file
        self.regexp = re.compile(r'(?P<lib_name>[\w_\-]+)==(?P<version>[\w\.\-]+)\s*#?(?P<comment>.*)')

    def get_from_requirements_folder(self, folder: Path):
        req_files = folder.glob('**/*.txt')
        global_req = dict()
        for req_file in req_files:
            reqs = self.get_from_requirement_file(req_file)
            global_req.update(reqs)
        return global_req

    def get_from_requirement_file(self, req_file: Path) -> Dict[str, RecommendedRequirement]:
        with open(req_file, 'r') as r_file:
            lines = r_file.readlines()
        parsed_requirements = dict()
        for i, line in enumerate(lines, 1):
            match = self.regexp.match(line)
            if match:
                lib_name = match.group('lib_name')
                versions = get_versions(lib_name)
                if len(versions) == 0:
                    raise Exception(f'Library {lib_name} not found')
                latest_version = versions[-1]
                recommended = RecommendedRequirement(name=lib_name, latest_version=latest_version,
                                                     approved_version=match.group('version'),
                                                     environment=req_file.stem)
                parsed_requirements[lib_name] = recommended
        return parsed_requirements


def parse_requirement_file(req_file: Path):
    regexp = re.compile(r'(?P<lib_name>[\w_\-]+)==(?P<version>[\w\.\-]+)\s*#?(?P<comment>.*)')
    with open(req_file, 'r') as r_file:
        lines = r_file.readlines()
    var_names = ['lib_name', 'version', 'comment']
    parsed_requirements = list()
    for i, line in enumerate(lines, 1):
        match = regexp.match(line)
        req = {'raw': line, 'line_number': i, 'parsed': None}
        if match:
            req['parsed'] = dict()
            for var_name in var_names:
                req['parsed'][var_name] = match.group(var_name)
        parsed_requirements.append(req)
    return parsed_requirements


def save_requirements_to_json(filename: Path, folder: Path):
    out_file = folder / 'reqs.json'
    reqs = parse_requirement_file(filename)

    with open(out_file, 'w') as d_file:
        json.dump(reqs, d_file)


def main2(requirements_folder: Path, folder: Path):
    out_file = folder / 'permitted.json'
    req_files = requirements_folder.glob('**/*.txt')
    global_req = dict()
    for req_file in req_files:
        reqs = parse_for_permitted_libs(req_file)
        global_req.update(reqs)
    with open(out_file, 'w') as d_file:
        json.dump(global_req, d_file)


if __name__ == '__main__':
    output_folder = Path(__file__).parent.parent.parent.parent / 'output'
    f = Path('/home/luiscberrocal/adelantos/adelantos-cupos/requirements/base.txt')
    save_requirements_to_json(f, output_folder)

    permitted_versions = output_folder / 'permitted_versions.json'
    f = Path('/home/luiscberrocal/adelantos/ec-d-local-payment-collector/requirements')
    main2(f, output_folder)
