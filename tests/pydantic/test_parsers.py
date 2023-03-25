from django_scaffolding_tools.parsers import parse_file_for_ast_classes
from django_scaffolding_tools.utils.core import quick_write


def test_parse_pydantic(fixtures_folder):
    pydantic_file = fixtures_folder / 'data_classes.py'
    ast_dict = parse_file_for_ast_classes(pydantic_file)
    write_intermediate = True
    if write_intermediate:
        model_filename = 'dc'
        quick_write(ast_dict, f'ast_{model_filename}.json', output_subfolder='pydantic')
