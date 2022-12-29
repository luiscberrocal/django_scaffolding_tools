import json

from django_scaffolding_tools._experimental.reqs_utilities.parsers import RequirementDatabase
from django_scaffolding_tools.utils.core import quick_write


class TestRequirementsDatabase:

    def test_r(self, output_folder, fixtures_folder):
        local_file = fixtures_folder / '_experimental' / 'requirements'
        json_db_file = output_folder / 'json_db.json'
        parsed = output_folder / '_local.json'
        db = RequirementDatabase(json_db_file)
        reqs = db.get_from_requirements_folder(local_file)
        reqs_dict = dict()
        for name, req in reqs.items():
            reqs_dict[name] = req.dict()
        with open(parsed, 'w') as f:
            json.dump(reqs_dict, f, indent=4, default=str)

    def test_get(self, fixtures_folder):
        json_db_file = fixtures_folder / '_experimental' / 'req_db.json'
        db = RequirementDatabase(json_db_file)
        req = db.get('django')
        assert req is not None
        assert req.approved_version == '3.2.16'

    def test_update_db(self, fixtures_folder):
        json_db_file = fixtures_folder / '_experimental' / 'req_db.json'
        db = RequirementDatabase(json_db_file)
        db.update_db()

    def test_add(self, fixtures_folder):
        json_db_file = fixtures_folder / '_experimental' / 'req_db.json'
        db = RequirementDatabase(json_db_file)
        db.add('django-test-plus', environment='local')
