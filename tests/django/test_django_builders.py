import pytest

from django_scaffolding_tools.django.builders import build_model_serializer_template_data
from django_scaffolding_tools.django.parsers import parse_for_django_classes
from django_scaffolding_tools.parsers import parse_file_for_ast_classes
from tests.test_parsers import quick_write


def test_build_model_serializer_template_data_camelize(output_folder, fixtures_folder):
    model_filename = 'simple_models2.py'
    filename = fixtures_folder / model_filename
    # 1 Convert model.py to an ast json file.
    ast_dict = parse_file_for_ast_classes(filename)
    quick_write(ast_dict, f'ast_{model_filename}.json', output_subfolder='django')
    # 2 Parse AST json dictionary for Django Model data
    model_data = parse_for_django_classes(ast_dict)
    quick_write(model_data, f'model_data_{model_filename}.json', output_subfolder='django')
    # 3 Build serializer data form Django model data
    serializer_data = build_model_serializer_template_data(model_data, add_source_camel_case=True)
    quick_write(serializer_data, f'serializer_data_{model_filename}.json', output_subfolder='django')
