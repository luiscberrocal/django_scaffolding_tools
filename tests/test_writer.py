from pathlib import Path

from django_scaffolding_tools.parsers import parse_file_for_ast_classes, parse_for_django_classes
from django_scaffolding_tools.writers import write_serializer_from_file, write_django_model_csv


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

