import json
from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def output_folder():
    folder = Path(__file__).parent.parent / 'output'
    return folder


@pytest.fixture(scope='session')
def camel_case_dict():
    data = {
        "firstName": "Luis",
        "lastName": "Wayne",
        "IMEI": "HJ8777"
    }
    return data


@pytest.fixture(scope='session')
def model_list_for_serializers():
    with open('./fixtures/model_list.json', 'r') as json_file:
        model_list = json.load(json_file)
    return model_list
