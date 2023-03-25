from pathlib import Path

from django_scaffolding_tools.django.writers import write_model_serializer_from_models_file, \
    write_model_factories_from_models_file


def test_write_model_serializer_from_models_file(fixtures_folder, output_folder):
    models_file = fixtures_folder / 'finance_models.py'
    serializer_file = output_folder / 'django' / 'serializers.py'
    write_model_serializer_from_models_file(models_file, serializer_file, camel_case=False)


def test_write_model_serializer_from_models_help(fixtures_folder, output_folder):
    models_file = fixtures_folder / 'models_with_helptext.py'
    models_file = output_folder / 'models.py'
    models_file = Path('/home/luiscberrocal/adelantos/bcp-integration/bcp_integration/api/models.py')
    serializer_file = output_folder / 'django' / 'serializers_2.py'
    write_model_serializer_from_models_file(models_file, serializer_file, write_intermediate=True, camel_case=False)

def test_write_model_factories_from_models_file(output_folder):
    models_file = Path('/home/luiscberrocal/PycharmProjects/alpha_clinic/alpha_clinic/patients/models.py')
    output_file = output_folder / 'django' / 'factories.py'
    write_model_factories_from_models_file(models_file, output_file, write_intermediate=True)
