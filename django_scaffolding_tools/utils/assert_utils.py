from datetime import datetime, date
from typing import Dict, Any, List
from typing import NamedTuple


class AssertionTuple(NamedTuple):
    var_name: str
    value: Any


def process_dict(data: Dict[str, Any], var_name: str) -> List[AssertionTuple]:
    assertion_list = list()
    for key, value in data.items():
        var_name_dict = f'{var_name}[\'{key}\']'
        if isinstance(value, dict):
            processed_list = process_dict(value, var_name_dict)
            assertion_list.extend(processed_list)
        else:
            processor_function = PROCESSOR_FUNCTIONS.get(type(value))
            if processor_function is not None:
                processed_list = processor_function(value, var_name_dict)
                assertion_list.extend(processed_list)

    return assertion_list


def process_datetime(data: datetime, var_name: str) -> List[AssertionTuple]:
    value = f'datetime({data.year}, {data.month}, {data.day}, {data.hour}, {data.minute},' \
            f' {data.second}, {data.microsecond})'

    return [AssertionTuple(var_name=var_name, value=value)]


def process_date(data: date, var_name: str) -> List[AssertionTuple]:
    value = f'date({data.year}, {data.month}, {data.day})'
    return [AssertionTuple(var_name=var_name, value=value)]


def process_str(data: str, var_name: str) -> List[AssertionTuple]:
    assertion_list = list()
    assertion_line = AssertionTuple(var_name=var_name, value=f"'{data}'")
    assertion_list.append(assertion_line)
    return assertion_list


def process_raw(data: Any, var_name: str) -> List[AssertionTuple]:
    return [AssertionTuple(var_name=var_name, value=data)]


def process_list(data: List[Any], var_name: str) -> List[AssertionTuple]:
    assertion_list = list()

    for i, value in enumerate(data):
        new_var_name = f'{var_name}[{i}]'
        processor_function = PROCESSOR_FUNCTIONS.get(type(value))
        if processor_function is not None:
            processed_list = processor_function(value, new_var_name)
            if len(processed_list) > 0:
                assertion_list.extend(processed_list)
    return assertion_list


PROCESSOR_FUNCTIONS = {
    datetime: process_datetime,
    date: process_date,
    dict: process_dict,
    str: process_str,
    int: process_raw,
    bool: process_raw,
    float: process_raw,
    list: process_list
}


def generate_assertion_tuples(data_dict: Dict[str, Any], var_name: str) -> List[AssertionTuple]:
    assertion_list = list()
    for key, value in data_dict.items():
        new_var_name = f'{var_name}[\'{key}\']'
        processor_function = PROCESSOR_FUNCTIONS.get(type(value))
        if processor_function is not None:
            processed_list = processor_function(value, new_var_name)
            if len(processed_list) > 0:
                assertion_list.extend(processed_list)
    return assertion_list


def generate_pytest_assertions(data_dict: Dict[str, Any], var_name: str) -> List[str]:
    pytest_assertion_list = list()
    assertion_list: List[AssertionTuple] = generate_assertion_tuples(data_dict, var_name)
    for assertion in assertion_list:
        if isinstance(assertion.value, bool):
            if assertion.value:
                assertion_message = f'assert {assertion.var_name}'
            else:
                assertion_message = f'assert not {assertion.var_name}'
        else:
            assertion_message = f'assert {assertion.var_name} == {assertion.value}'
        print(assertion_message)
        pytest_assertion_list.append(assertion_message)
    return pytest_assertion_list
