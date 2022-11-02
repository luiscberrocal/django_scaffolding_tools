from pathlib import Path

from django_scaffolding_tools.django.builders import build_model_serializer_template_data
from django_scaffolding_tools.django.parsers import parse_for_django_classes
from django_scaffolding_tools.parsers import parse_file_for_ast_classes
from django_scaffolding_tools.writers import ReportWriter
from tests.test_parsers import quick_write


def write_model_serializer_from_models_file(models_file: Path, output_file: Path, write_intermediate: bool = False):
    """Parses a Django model.py file and generates the selializer for all the models."""
    # 1 Convert model.py to an ast json file.
    ast_dict = parse_file_for_ast_classes(models_file)
    if write_intermediate:
        model_filename = 'models.py'
        quick_write(ast_dict, f'ast_{model_filename}.json', output_subfolder='django')
    # 2 Parse AST json dictionary for Django Model data
    model_data = parse_for_django_classes(ast_dict)
    if write_intermediate:
        model_filename = 'models.py'
        quick_write(model_data, f'model_data_{model_filename}.json', output_subfolder='django')
    # 3 Build serializer data form Django model data
    serializer_data = build_model_serializer_template_data(model_data, add_source_camel_case=False)
    if write_intermediate:
        model_filename = 'models.py'
        quick_write(serializer_data, f'serializer_data_{model_filename}.json', output_subfolder='django')
    template_data = {'classes': serializer_data}
    writer = ReportWriter()
    writer.write('drf_model_serializers.py.j2', output_file, template_data=template_data)
