import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Union, List

from django_scaffolding_tools.builders import build_serializer_template_data, build_serializer_data
from django_scaffolding_tools.parsers import parse_dict, transform_dict_to_model_list, parse_for_patterns, \
    parse_file_for_ast_classes, parse_for_django_classes
from django_scaffolding_tools.patterns import PATTERN_FUNCTIONS
from django_scaffolding_tools.writers import ReportWriter


def quick_write(data: Union[Dict[str, Any], List[Dict[str, Any]]], file: str, over_write: bool = True):
    def quick_serialize(value):
        return f'{value}'

    filename = Path(__file__).parent.parent / 'output' / file

    if (filename.exists() and over_write) or not filename.exists():
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4, default=quick_serialize)
        return filename


def test_simple_parsing(output_folder):
    data = {
        "id": "D-4-be8eda8c-5fe7-49dd-8058-4ddaac00611b",
        "amount": 72.00,
        "status": "PAID",
        "status_detail": "The payment was paid.",
        "status_code": "200",
        "currency": "USD",
        "country": "AR",
        "payment_method_id": "RP",
        "payment_method_type": "TICKET",
        "payment_method_flow": "REDIRECT",
        "payer": {
            "name": "Nino Deicas",
            "user_reference": "US-jmh3gb4kj5h34",
            "email": "buyer@gmail.com",
            "address": {
                "street": "123th street",
                "state": "FL",
                "zip_code": "99999999"
            }
        },
        "order_id": "4m1OdghPUQtg",
        "notification_url": "http://www.merchant.com/notifications",
        "created_date": "2019-06-26T15:17:31.000+0000",
        "user": {
            "id": 1,
            "username": "bwayne",
            "created": datetime.now()
        }
    }
    # 1. Parse raw dictionary
    parsed_dict = parse_dict(data)
    quick_write(parsed_dict, 'parsed.json')
    # 2. Transform dictionary to a list of models
    model_list = transform_dict_to_model_list(parsed_dict)
    model_list = parse_for_patterns(model_list, PATTERN_FUNCTIONS)
    model_list = build_serializer_data(model_list)

    quick_write(model_list, 'model_list.json')
    template_model_list = build_serializer_template_data(model_list)
    quick_write(template_model_list, 'template_model_list.json')

    writer = ReportWriter()
    output_file = output_folder / 'serializers.py'
    writer.write('drf_serializers.py.j2', output_file, template_data=template_model_list)
    assert output_file.exists()


def test_simple_parsing_camel_case(output_folder, camel_case_dict):
    parsed_dict = parse_dict(camel_case_dict)
    quick_write(parsed_dict, 'parsed_camel_case.json')

    model_list = transform_dict_to_model_list(parsed_dict)
    model_list = parse_for_patterns(model_list, PATTERN_FUNCTIONS)
    model_list = build_serializer_data(model_list)

    quick_write(model_list, 'model_list_camel_case.json')

    template_model_list = build_serializer_template_data(model_list)
    quick_write(template_model_list, 'template_camel_case_model_list.json')

    writer = ReportWriter()
    output_file = output_folder / 'serializers_camel_case.py'
    writer.write('drf_serializers.py.j2', output_file, template_data=template_model_list)
    assert output_file.exists()


def test_class_list(fixtures_folder, output_folder):
    module_file = 'models.py'
    filename = fixtures_folder / module_file

    ast_module = parse_file_for_ast_classes(filename)
    quick_write(ast_module, f'ast_{module_file}.json')

    django_classes = parse_for_django_classes(ast_module)
    quick_write(django_classes, f'ast_classes_{module_file}.json')
