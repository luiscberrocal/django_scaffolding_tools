import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from django_scaffolding_tools.parsers import parse_dict, transform_dict_to_model_list, post_process_attributes


def quick_write(data: Dict[str, Any], file:str):
    def quick_serialize(value):
        return f'{value}'

    filename = Path(__file__).parent.parent / 'output' / file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4, default=quick_serialize)
    return filename


def test_simple_parsing():
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
    parsed_dict = parse_dict(data)
    quick_write(parsed_dict, 'parsed.json')

    model_list = transform_dict_to_model_list(parsed_dict)
    model_list = post_process_attributes(model_list)
    quick_write(model_list, 'model_list.json')

