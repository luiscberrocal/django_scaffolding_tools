from django_scaffolding_tools.django.writers import write_model_serializer_from_models_file


def test_write_model_serializer_from_models_file(fixtures_folder, output_folder):
    models_file = fixtures_folder / 'finance_models.py'
    serializer_file = output_folder / 'django' / 'serializers.py'
    write_model_serializer_from_models_file(models_file, serializer_file, camel_case=False)
def test_write_model_serializer_from_models_help(fixtures_folder, output_folder):
    models_file = fixtures_folder / 'models_with_helptext.py'
    serializer_file = output_folder / 'django' / 'serializers.py'
    write_model_serializer_from_models_file(models_file, serializer_file, write_intermediate=True, camel_case=False)
