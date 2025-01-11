from datetime import datetime
from pathlib import Path

from django_scaffolding_tools.django.builders import build_model_serializer_template_data
from django_scaffolding_tools.django.handlers import (
    IntegerFieldHandler,
    CharFieldHandler,
    ForeignKeyFieldHandler,
    DateFieldHandler,
    DateTimeFieldHandler,
    DecimalFieldHandler,
    BooleanFieldHandler,
    DateTimeCharFieldHandler,
    EmailFieldHandler,
    JSONFieldHandler,
)
from django_scaffolding_tools.django.parsers import parse_for_django_classes
from django_scaffolding_tools.parsers import parse_file_for_ast_classes
from django_scaffolding_tools.writers import ReportWriter
from django_scaffolding_tools.utils.core import quick_write


def write_model_serializer_from_models_file(
    models_file: Path, output_file: Path, write_intermediate: bool = False, camel_case=False
):
    """Parses a Django models.py file and generates the serializer for all the models."""
    # 1 Convert model.py to an ast json file.
    ast_dict = parse_file_for_ast_classes(models_file)
    if write_intermediate:
        model_filename = "models.py"
        quick_write(ast_dict, f"ast_{model_filename}.json", output_subfolder="django")
    # 2 Parse AST json dictionary for Django Model data
    model_data = parse_for_django_classes(ast_dict)
    if write_intermediate:
        model_filename = "models.py"
        quick_write(model_data, f"model_data_{model_filename}.json", output_subfolder="django")
    # 3 Build serializer data form Django model data
    serializer_data = build_model_serializer_template_data(model_data, add_source_camel_case=camel_case)
    if write_intermediate:
        model_filename = "models.py"
        quick_write(serializer_data, f"serializer_data_{model_filename}.json", output_subfolder="django")
    writer = ReportWriter()
    writer.write("drf_model_serializers.py.j2", output_file, template_data=serializer_data)


def write_model_factories_from_models_file(
    models_file: Path, output_file: Path, write_intermediate: bool = False, camel_case=False
):
    """Parses a Django models.py file and generates the serializer for all the models."""
    # 1 Convert model.py to an ast json file.
    ast_dict = parse_file_for_ast_classes(models_file)
    if write_intermediate:
        model_filename = "models.py"
        quick_write(ast_dict, f"ast_{model_filename}.json", output_subfolder="django")
    # 2 Parse AST json dictionary for Django Model data
    model_data = parse_for_django_classes(ast_dict)
    if write_intermediate:
        model_filename = "models.py"
        quick_write(model_data, f"model_data_{model_filename}.json", output_subfolder="django")
    handlers = [
        IntegerFieldHandler(),
        CharFieldHandler(),
        DateTimeCharFieldHandler(),
        ForeignKeyFieldHandler(),
        DateFieldHandler(),
        DateTimeFieldHandler(),
        DecimalFieldHandler(),
        BooleanFieldHandler(),
        EmailFieldHandler(),
        JSONFieldHandler(),
    ]

    for i in range(len(handlers)):
        if i < len(handlers) - 1:
            handlers[i].set_next(handlers[i + 1])

    main_handler = handlers[0]
    lines = list()
    imports = f"""# Generated with django_scaffolding_tool {datetime.now()}
import string
from datetime import datetime

from django.utils import timezone
from factory import Iterator, SelfAttribute, Trait
from factory import LazyAttribute
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from faker import Factory as FakerFactory

faker = FakerFactory.create()\n"""
    lines.append(imports)
    for fp_data in model_data["classes"]:
        lines.append(f'class {fp_data["name"]}Factory(DjangoModelFactory):\n')
        lines.append(f"\tclass Meta:\n")
        lines.append(f'\t\tmodel = {fp_data["name"]}\n')
        lines.append("\n")
        for att in fp_data["attributes"]:
            result = main_handler.handle(att)
            if result is None:
                lines.append(f'\t# {att["name"]} {att["data_type"]} NOT supported\n')
            else:
                lines.append(f'\t{result["name"]} = {result["factory_field"]}\n')
        lines.append("\n")
        # lines.append("#" * 80)
    with open(output_file, "w") as py_file:
        py_file.writelines(lines)
