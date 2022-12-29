import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict

import requests
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
        self.database = dict()
        self.load_db(self.source_file)

    def load_db(self, source_file: Path):
        with open(source_file, 'r') as j_file:
            data = json.load(j_file)
        for name, req_dict in data.items():
            self.database[name] = RecommendedRequirement(**req_dict)

    def get(self, name: str):
        return self.database.get(name)

    def update_db(self, commit: bool = True):
        for name, req in self.database.items():
            info = self._download_info(name, req.approved_version)
            req.home_page = info['home_page']
            req.license = info['license']
            req.last_updated = datetime.now()
        if commit:
            self.save()

    def _download_info(self, name: str, version: str):
        url = f'https://pypi.org/pypi/{name}/{version}/json'
        response = requests.get(url)
        info = dict()
        if response.status_code == 200:
            data = response.json()
            home_page = data['info']['home_page']
            lic = data['info']['license']
            info = {'home_page': home_page, 'license': lic}
        return info

    def save(self):
        tmp = dict()
        for name, req in self.database.items():
            tmp[name] = req.dict()

        with open(self.source_file, 'w') as f:
            json.dump(tmp, f, indent=4, default=str)

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
