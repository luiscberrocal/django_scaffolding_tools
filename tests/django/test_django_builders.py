import pytest

from django_scaffolding_tools.django.builders import build_model_serializer_template_data
from django_scaffolding_tools.django.parsers import parse_for_django_classes
from django_scaffolding_tools.parsers import parse_file_for_ast_classes
from django_scaffolding_tools.utils.assert_utils import generate_pytest_assertions
from django_scaffolding_tools.utils.core import quick_write


def test_build_model_serializer_template_data_camelize(output_folder, fixtures_folder):
    model_filename = 'simple_models2.py'
    filename = fixtures_folder / model_filename
    # 1 Convert model.py to an ast json file.
    ast_dict = parse_file_for_ast_classes(filename)
    # 2 Parse AST json dictionary for Django Model data
    model_data = parse_for_django_classes(ast_dict)
    # 3 Build serializer data form Django model data
    serializer_data = build_model_serializer_template_data(model_data, add_source_camel_case=True)

    quick_write(ast_dict, f'ast_{model_filename}.json', output_subfolder='django')
    quick_write(model_data, f'model_data_{model_filename}.json', output_subfolder='django')
    quick_write(serializer_data, f'serializer_data_{model_filename}.json', output_subfolder='django')

    assert len(serializer_data) == 2

    model1 = serializer_data[0]
    assert model1['model'] == 'Clinic'
    assert model1['fields'][0]['name'] == 'name'
    assert model1['fields'][0]['serializer'] == 'serializers.CharField()'

    model2 = serializer_data[1]
    assert model2['model'] == 'Patient'
    assert model2['fields'][0]['name'] == 'first_name'
    assert model2['fields'][0]['source'] == 'firstName'
    assert model2['fields'][0]['serializer'] == 'serializers.CharField(source=\'firstName\')'
    assert model2['fields'][1]['name'] == 'last_name'
    assert model2['fields'][1]['source'] == 'lastName'
    assert model2['fields'][1]['serializer'] == 'serializers.CharField(source=\'lastName\')'
    assert model2['fields'][2]['name'] == 'owning_clinic'
    assert model2['fields'][2]['source'] == 'owningClinic'
    assert model2['fields'][2]['serializer'] == 'ClinicSerializer(source=\'owningClinic\', read_only=True)'


def test_build_model_serializer_template_data(output_folder, fixtures_folder):
    model_filename = 'simple_models2.py'
    filename = fixtures_folder / model_filename
    # 1 Convert model.py to an ast json file.
    ast_dict = parse_file_for_ast_classes(filename)
    # 2 Parse AST json dictionary for Django Model data
    model_data = parse_for_django_classes(ast_dict)
    # 3 Build serializer data form Django model data
    serializer_data = build_model_serializer_template_data(model_data, add_source_camel_case=False)

    quick_write(ast_dict, f'ast_{model_filename}.json', output_subfolder='django')
    quick_write(model_data, f'model_data_{model_filename}.json', output_subfolder='django')
    quick_write(serializer_data, f'serializer_data_{model_filename}.json', output_subfolder='django')

    assert len(serializer_data) == 2

    model1 = serializer_data[0]
    assert model1['model'] == 'Clinic'
    assert model1['fields'][0]['name'] == 'name'
    assert model1['fields'][0]['serializer'] == 'serializers.CharField()'

    model2 = serializer_data[1]
    assert model2['model'] == 'Patient'
    assert model2['fields'][0]['name'] == 'first_name'
    assert model2['fields'][0]['serializer'] == 'serializers.CharField()'
    assert model2['fields'][1]['name'] == 'last_name'
    assert model2['fields'][1]['serializer'] == 'serializers.CharField()'
    assert model2['fields'][2]['name'] == 'owning_clinic'
    assert model2['fields'][2]['serializer'] == 'ClinicSerializer()'
