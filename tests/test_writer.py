from pathlib import Path

from django_scaffolding_tools.parsers import parse_file_for_ast_classes
from django_scaffolding_tools.django.parsers import parse_for_django_classes
from django_scaffolding_tools.writers import write_serializer_from_file, write_django_model_csv, \
    simple_write_to_excel, write_django_model_excel


def test_write_serializers(output_folder):
    source_filename = Path(__file__).parent / 'fixtures' / 'json_data.json'
    assert source_filename.exists()

    target_file = output_folder / 'test_write_serializers.py'
    write_serializer_from_file(source_filename, target_file)
    assert target_file.exists()


def test_write_django_model_csv(output_folder, fixtures_folder):
    csv_filename = output_folder / 'model.csv'
    module_file = 'models_with_helptext.py'
    filename = fixtures_folder / module_file

    ast_module = parse_file_for_ast_classes(filename)
    django_classes = parse_for_django_classes(ast_module)
    write_django_model_csv(django_classes['classes'], csv_filename)


def test_simple_excel_writer(output_folder):
    headers = {'name': {'title': 'Name'}, 'phone_number': {'title': 'Phone number'},
               'monthly_payment': {'title': 'Monthly payment'}}
    data = [
        {'name': 'Bruce Wayne', 'phone_number': '89765400', 'monthly_payment': 234.34},
        {'name': 'Clark Kent', 'phone_number': '19765400', 'monthly_payment': 34.34},
        {'name': 'Luke Cage', 'phone_number': '99765400', 'monthly_payment': 23.34},
        {'name': 'Stephen Strange', 'phone_number': '49765400', 'monthly_payment': 234.34},
    ]
    filename = output_folder / 'excel_output.xlsx'
    simple_write_to_excel(filename, headers, data)


def test_write_django_model_excel(output_folder, fixtures_folder):
    xlsx_filename = output_folder / 'model.xlsx'
    module_file = 'models_with_helptext.py'
    filename = fixtures_folder / module_file

    ast_module = parse_file_for_ast_classes(filename)
    django_classes = parse_for_django_classes(ast_module)
    write_django_model_excel(django_classes['classes'], xlsx_filename)
