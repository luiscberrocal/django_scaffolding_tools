from django_scaffolding_tools.django.writers import write_model_serializer_from_models_file


def test_write_model_serializer_from_models_file(fixtures_folder, output_folder):
    models_file = fixtures_folder / 'simple_models2.py'
    serializer_file = output_folder / 'django' / 'serializers.py'
    write_model_serializer_from_models_file(models_file, serializer_file, camel_case=True)
