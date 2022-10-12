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
        "lastName": "Wayne"
    }
    return data
