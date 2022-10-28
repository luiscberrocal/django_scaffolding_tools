import collections
from datetime import datetime, date
from decimal import Decimal
from typing import Dict, Any, List, NamedTuple

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Any, List


def write_assertions(dictionary_list, variable_name, **kwargs):
    """
    Writes assertions using Django practice of putting actual value first and then expected value to a file.
    If no filename is supplied it will generate a file in the settings.TEST_OUTPUT_PATH folder with the
    **variable_name** and the current date.
    By default key named created and modified will be excluded.

    :param dictionary_list: <list> or <dict> dictionary or list of values
    :param variable_name: <str> name of the variable
    :param kwargs:  filename <str>String. Full path to the output file.
    :param kwargs:  excluded_keys <list>list of strings. List with keys to exclude
    :param kwargs:  type_only <boolean> Check only for types instead of values. Default false
    :return: filename string.
    """
    writer = AssertionWriter(**kwargs)
    return writer.write_assert_list(dictionary_list, variable_name, filename=kwargs.get('filename'))


class AssertionWriter(object):
    """
    This class generates assertions using Django practice of putting actual value first and then expected value.
    """

    def __init__(self, **kwargs):
        self.excluded_variable_names = ['created', 'modified']
        if kwargs.get('excluded_keys') is not None:
            for key in kwargs.get('excluded_keys'):
                self.excluded_variable_names.append(key)

        self.use_regexp_assertion = kwargs.get('use_regexp_assertion', False)

        self.common_regexp = []  # FIXME Copied from django_test_tools

        self.check_for_type_only = kwargs.get('type_only', False)

    def add_regular_expression(self, name, pattern, **kwargs):
        self.common_regexp.add_regular_expression(name, pattern, **kwargs)

    def write_assert_list(self, dictionary_list, variable_name, **kwargs):
        """
        Function to generate assertions for a dictionary or list content.
        :param kwargs:
        :param dictionary_list:
        :param variable_name:
        :return:
        """
        if kwargs.get('filename') is None:
            filename = '{}.py'.format(variable_name)
        else:
            filename = kwargs.get('filename')
        if self.check_for_type_only:
            if isinstance(dictionary_list, dict):
                assert_list = self._generate_assert_type_dictionaries(dictionary_list, variable_name)
            elif isinstance(dictionary_list, list):
                assert_list = self._generate_assert_type_list(dictionary_list, variable_name)
        else:
            if isinstance(dictionary_list, dict):
                assert_list = self._generate_assert_equals_dictionaries(dictionary_list, variable_name)
            elif isinstance(dictionary_list, list):
                assert_list = self._generate_assert_equals_list(dictionary_list, variable_name)

        with open(filename, 'w', encoding='utf-8', newline='\n') as python_file:
            python_file.write('\n'.join(assert_list))

        return filename

    def _generate_assert_equals_list(self, data_list, variable_name, indentation_level=0):
        assert_list = list()
        if variable_name not in self.excluded_variable_names:
            index = 0
            # assert_list.append('# ********** variable {} ***********'.format(variable_name))
            assert_list.append('self.assertEqual({}, {})'.format('len({})'.format(variable_name), len(data_list)))
            for data in data_list:
                list_variable = '{}[{}]'.format(variable_name, index)
                self._build_equals_assertion(list_variable, data, assert_list)
                index += 1
        return assert_list

    def _generate_assert_equals_dictionaries(self, dictionary, variable_name, **kwargs):
        assert_list = list()
        if variable_name not in self.excluded_variable_names:
            ordered_dictionary = collections.OrderedDict(sorted(dictionary.items()))
            for key, value in ordered_dictionary.items():
                if key not in self.excluded_variable_names:
                    dict_variable = '{}[\'{}\']'.format(variable_name, key)
                    self._build_equals_assertion(dict_variable, value, assert_list)
        return assert_list

    def _build_equals_assertion(self, variable_name, data, assert_list):
        if variable_name not in self.excluded_variable_names:
            if isinstance(data, str):
                data = data.translate(str.maketrans({"'": '\\\''}))
                if self.use_regexp_assertion:
                    pattern = self.common_regexp.match_regexp(data)[0]
                    if pattern is None:
                        assert_list.append('self.assertEqual({}, \'{}\')'.format(variable_name, data))
                    else:
                        assert_list.append('self.assertRegex({}, r\'{}\')'.format(variable_name, pattern))
                else:
                    assert_list.append('self.assertEqual({}, \'{}\')'.format(variable_name, data))
            elif isinstance(data, datetime):
                date_time_format = '%Y-%m-%d %H:%M:%S%z'
                str_datetime = data.strftime(date_time_format)
                assert_list.append(
                    'self.assertEqual({}.strftime(\'{}\'), \'{}\')'.format(
                        variable_name,
                        date_time_format,
                        str_datetime,
                    )
                )
            elif isinstance(data, date):
                date_format = '%Y-%m-%d'
                str_date = data.strftime(date_format)
                assert_list.append(
                    'self.assertEqual({}.strftime(\'{}\'), \'{}\')'.format(variable_name, date_format, str_date))
            elif isinstance(data, Decimal):
                assert_list.append('self.assertEqual({}, Decimal({}))'.format(variable_name, data))
            elif isinstance(data, list):
                assert_list += self._generate_assert_equals_list(data, variable_name)
            elif isinstance(data, dict):
                assert_list += self._generate_assert_equals_dictionaries(data, variable_name)
            else:
                assert_list.append('self.assertEqual({}, {})'.format(variable_name, data))

    def _build_type_assertion(self, variable_name, data, assert_list):
        if variable_name not in self.excluded_variable_names:
            if isinstance(data, str):
                assert_list.append('self.assertIsNotNone({}) # Example: {}'.format(variable_name, data))
            elif isinstance(data, datetime):
                date_time_format = '%Y-%m-%d %H:%M:%S%z'
                datetime_regexp = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))\s\d{2}:\d{2}:\d{2}\+\d{4}'
                str_datetime = data.strftime(date_time_format)
                assert_list.append(
                    'self.assertRegex({}.strftime(\'{}\'), r\'{}\') # Example: {}'.format(
                        variable_name,
                        date_time_format,
                        datetime_regexp,
                        str_datetime,
                    )
                )
            elif isinstance(data, date):
                date_format = '%Y-%m-%d'
                date_regexp = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
                str_date = data.strftime(date_format)
                assert_list.append(
                    'self.assertRegex({}.strftime(\'{}\'), r\'{}\') # Example: {}'.format(
                        variable_name,
                        date_format,
                        date_regexp,
                        str_date))
            elif isinstance(data, Decimal):
                assert_list.append('self.assertIsNotNone({}) # Example: Decimal({})'.format(variable_name, data))
            elif isinstance(data, list):
                assert_list += self._generate_assert_type_list(data, variable_name)
            elif isinstance(data, dict):
                assert_list += self._generate_assert_type_dictionaries(data, variable_name)
            else:
                if data is None:
                    assert_list.append('self.assertIsNone({}) # Example: {}'.format(variable_name, data))
                else:
                    assert_list.append('self.assertIsNotNone({}) # Example: {}'.format(variable_name, data))

    def _generate_assert_type_dictionaries(self, dictionary, variable_name, **kwargs):
        assert_list = list()
        assert_list.append('self.assertEqual(len({}.keys()), {})'.format(variable_name, len(dictionary.keys())))
        if variable_name not in self.excluded_variable_names:
            ordered_dictionary = collections.OrderedDict(sorted(dictionary.items()))
            for key, value in ordered_dictionary.items():
                if key not in self.excluded_variable_names:
                    dict_variable = '{}[\'{}\']'.format(variable_name, key)
                    self._build_type_assertion(dict_variable, value, assert_list)
        return assert_list

    def _generate_assert_type_list(self, data_list, variable_name, indentation_level=0):
        assert_list = list()
        if variable_name not in self.excluded_variable_names:
            index = 0
            # assert_list.append('# ********** variable {} ***********'.format(variable_name))
            assert_list.append('self.assertEqual({}, {})'.format('len({})'.format(variable_name), len(data_list)))
            for data in data_list:
                list_variable = '{}[{}]'.format(variable_name, index)
                self._build_type_assertion(list_variable, data, assert_list)
                index += 1
        return assert_list


class AssertionTuple(NamedTuple):
    var_name: str
    value: Any


def process_dict(data: Dict[str, Any], var_name: str) -> List[AssertionTuple]:
    print(f'{var_name}: {data}')
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


def process_str(data: str, var_name: str) -> List[AssertionTuple]:
    assertion_list = list()
    assertion_line = AssertionTuple(var_name=var_name, value=f"'{data}'")
    assertion_list.append(assertion_line)
    return assertion_list


def process_raw(data: Any, var_name: str) -> List[AssertionTuple]:
    return [AssertionTuple(var_name=var_name, value=data)]


PROCESSOR_FUNCTIONS = {
    datetime: process_datetime,
    dict: process_dict,
    str: process_str,
    int: process_raw,
    bool: process_raw,
    float: process_raw,
}


def generate_dict_assertions(data_dict: Dict[str, Any], var_name: str) -> List[NamedTuple]:
    assertion_list = list()
    for key, value in data_dict.items():
        var_name_dict = f'{var_name}[\'{key}\']'
        processor_function = PROCESSOR_FUNCTIONS.get(type(value))
        if processor_function is not None:
            processed_list = processor_function(value, var_name_dict)
            if len(processed_list) > 0:
                assertion_list.extend(processed_list)
    return assertion_list
