from django_scaffolding_tools._experimental.reqs_utilities.parsers import RequirementDatabase
from django_scaffolding_tools.utils.core import quick_write


class TestRequirementsDatabase:

    def test_r(self, output_folder, fixtures_folder):
        local_file = fixtures_folder / '_experimental' / 'requirements' / 'local.txt'
        json_db_file = output_folder / 'json_db.json'
        json_db_file = output_folder / 'local.json'
        db = RequirementDatabase(json_db_file)
        reqs = db.get_from_requirement_file(local_file)
        quick_write(reqs, '_r.json')
