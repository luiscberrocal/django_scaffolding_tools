import json
from datetime import datetime

import humps
import pytest

from django_scaffolding_tools.builders import build_serializer_template_data, build_serializer_data
from django_scaffolding_tools.parsers import parse_dict, transform_dict_to_model_list, parse_for_patterns, \
    parse_file_for_ast_classes, parse_var_name
from django_scaffolding_tools.patterns import PATTERN_FUNCTIONS
from django_scaffolding_tools.utils.core import quick_write
from django_scaffolding_tools.writers import ReportWriter


class TestParseDataDictionary:

    def test_parse(self, d_local_data_dict):
        parsed_dict = parse_dict(d_local_data_dict, model_name='Payment')

        assert parsed_dict['payment']['level'] == 0
        assert parsed_dict['payment']['attributes'][0]['name'] == 'id'
        assert parsed_dict['payment']['attributes'][0]['value'] == 'D-4-be8eda8c-5fe7-49dd-8058-4ddaac00611b'
        assert parsed_dict['payment']['attributes'][0]['supported']
        assert parsed_dict['payment']['attributes'][0]['native']
        assert not parsed_dict['payment']['attributes'][0]['many']
        assert parsed_dict['payment']['attributes'][0]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][0]['length'] == 40
        assert parsed_dict['payment']['attributes'][1]['name'] == 'amount'
        assert parsed_dict['payment']['attributes'][1]['value'] == 72.0
        assert parsed_dict['payment']['attributes'][1]['supported']
        assert parsed_dict['payment']['attributes'][1]['native']
        assert not parsed_dict['payment']['attributes'][1]['many']
        assert parsed_dict['payment']['attributes'][1]['data_type'] == 'float'
        assert parsed_dict['payment']['attributes'][2]['name'] == 'status'
        assert parsed_dict['payment']['attributes'][2]['value'] == 'PAID'
        assert parsed_dict['payment']['attributes'][2]['supported']
        assert parsed_dict['payment']['attributes'][2]['native']
        assert not parsed_dict['payment']['attributes'][2]['many']
        assert parsed_dict['payment']['attributes'][2]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][2]['length'] == 4
        assert parsed_dict['payment']['attributes'][3]['name'] == 'status_detail'
        assert parsed_dict['payment']['attributes'][3]['value'] == 'The payment was paid.'
        assert parsed_dict['payment']['attributes'][3]['supported']
        assert parsed_dict['payment']['attributes'][3]['native']
        assert not parsed_dict['payment']['attributes'][3]['many']
        assert parsed_dict['payment']['attributes'][3]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][3]['length'] == 21
        assert parsed_dict['payment']['attributes'][4]['name'] == 'status_code'
        assert parsed_dict['payment']['attributes'][4]['value'] == '200'
        assert parsed_dict['payment']['attributes'][4]['supported']
        assert parsed_dict['payment']['attributes'][4]['native']
        assert not parsed_dict['payment']['attributes'][4]['many']
        assert parsed_dict['payment']['attributes'][4]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][4]['length'] == 3
        assert parsed_dict['payment']['attributes'][5]['name'] == 'currency'
        assert parsed_dict['payment']['attributes'][5]['value'] == 'USD'
        assert parsed_dict['payment']['attributes'][5]['supported']
        assert parsed_dict['payment']['attributes'][5]['native']
        assert not parsed_dict['payment']['attributes'][5]['many']
        assert parsed_dict['payment']['attributes'][5]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][5]['length'] == 3
        assert parsed_dict['payment']['attributes'][6]['name'] == 'country'
        assert parsed_dict['payment']['attributes'][6]['value'] == 'AR'
        assert parsed_dict['payment']['attributes'][6]['supported']
        assert parsed_dict['payment']['attributes'][6]['native']
        assert not parsed_dict['payment']['attributes'][6]['many']
        assert parsed_dict['payment']['attributes'][6]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][6]['length'] == 2
        assert parsed_dict['payment']['attributes'][7]['name'] == 'payment_method_id'
        assert parsed_dict['payment']['attributes'][7]['value'] == 'RP'
        assert parsed_dict['payment']['attributes'][7]['supported']
        assert parsed_dict['payment']['attributes'][7]['native']
        assert not parsed_dict['payment']['attributes'][7]['many']
        assert parsed_dict['payment']['attributes'][7]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][7]['length'] == 2
        assert parsed_dict['payment']['attributes'][8]['name'] == 'payment_method_type'
        assert parsed_dict['payment']['attributes'][8]['value'] == 'TICKET'
        assert parsed_dict['payment']['attributes'][8]['supported']
        assert parsed_dict['payment']['attributes'][8]['native']
        assert not parsed_dict['payment']['attributes'][8]['many']
        assert parsed_dict['payment']['attributes'][8]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][8]['length'] == 6
        assert parsed_dict['payment']['attributes'][9]['name'] == 'payment_method_flow'
        assert parsed_dict['payment']['attributes'][9]['value'] == 'REDIRECT'
        assert parsed_dict['payment']['attributes'][9]['supported']
        assert parsed_dict['payment']['attributes'][9]['native']
        assert not parsed_dict['payment']['attributes'][9]['many']
        assert parsed_dict['payment']['attributes'][9]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][9]['length'] == 8
        assert parsed_dict['payment']['attributes'][10]['name'] == 'payer'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['name'] == 'Payer'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['level'] == 1
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][0]['name'] == 'name'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][0]['value'] == 'Nino Deicas'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][0]['supported']
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][0]['native']
        assert not parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][0]['many']
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][0]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][0]['length'] == 11
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][1]['name'] == 'user_reference'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][1][
                   'value'] == 'US-jmh3gb4kj5h34'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][1]['supported']
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][1]['native']
        assert not parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][1]['many']
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][1]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][1]['length'] == 16
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][2]['name'] == 'email'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][2]['value'] == 'buyer@gmail.com'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][2]['supported']
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][2]['native']
        assert not parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][2]['many']
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][2]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][2]['length'] == 15
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['name'] == 'address'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                   'name'] == 'Address'
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                   'level'] == 2
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][0][
                'name'] == 'street'
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][0][
                'value'] == '123th street'
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][0][
                'supported']
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][0][
                'native']
        assert not \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][0][
                'many']
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][0][
                'data_type'] == 'str'
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][0][
                'length'] == 12
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][1][
                'name'] == 'state'
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][1][
                'value'] == 'FL'
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][1][
                'supported']
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][1][
                'native']
        assert not \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][1][
                'many']
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][1][
                'data_type'] == 'str'
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][1][
                'length'] == 2
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][2][
                'name'] == 'zip_code'
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][2][
                'value'] == '99999999'
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][2][
                'supported']
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][2][
                'native']
        assert not \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][2][
                'many']
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][2][
                'data_type'] == 'str'
        assert \
            parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['value']['address'][
                'attributes'][2][
                'length'] == 8
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['supported']
        assert not parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['native']
        assert not parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['many']
        assert parsed_dict['payment']['attributes'][10]['value']['payer']['attributes'][3]['data_type'] == 'Address'
        assert parsed_dict['payment']['attributes'][10]['supported']
        assert not parsed_dict['payment']['attributes'][10]['native']
        assert not parsed_dict['payment']['attributes'][10]['many']
        assert parsed_dict['payment']['attributes'][10]['data_type'] == 'Payer'
        assert parsed_dict['payment']['attributes'][11]['name'] == 'order_id'
        assert parsed_dict['payment']['attributes'][11]['value'] == '4m1OdghPUQtg'
        assert parsed_dict['payment']['attributes'][11]['supported']
        assert parsed_dict['payment']['attributes'][11]['native']
        assert not parsed_dict['payment']['attributes'][11]['many']
        assert parsed_dict['payment']['attributes'][11]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][11]['length'] == 12
        assert parsed_dict['payment']['attributes'][12]['name'] == 'notification_url'
        assert parsed_dict['payment']['attributes'][12]['value'] == 'http://www.merchant.com/notifications'
        assert parsed_dict['payment']['attributes'][12]['supported']
        assert parsed_dict['payment']['attributes'][12]['native']
        assert not parsed_dict['payment']['attributes'][12]['many']
        assert parsed_dict['payment']['attributes'][12]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][12]['length'] == 37
        assert parsed_dict['payment']['attributes'][13]['name'] == 'created_date'
        assert parsed_dict['payment']['attributes'][13]['value'] == '2019-06-26T15:17:31.000+0000'
        assert parsed_dict['payment']['attributes'][13]['supported']
        assert parsed_dict['payment']['attributes'][13]['native']
        assert not parsed_dict['payment']['attributes'][13]['many']
        assert parsed_dict['payment']['attributes'][13]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][13]['length'] == 28
        assert parsed_dict['payment']['attributes'][14]['name'] == 'user'
        assert parsed_dict['payment']['attributes'][14]['value']['user']['name'] == 'User'
        assert parsed_dict['payment']['attributes'][14]['value']['user']['level'] == 1
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][0]['name'] == 'id'
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][0]['value'] == 1
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][0]['supported']
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][0]['native']
        assert not parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][0]['many']
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][0]['data_type'] == 'int'
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][1]['name'] == 'username'
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][1]['value'] == 'bwayne'
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][1]['supported']
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][1]['native']
        assert not parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][1]['many']
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][1]['data_type'] == 'str'
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][1]['length'] == 6
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][2]['name'] == 'created'
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][2]['value'] == datetime(2022, 10,
                                                                                                               21, 11,
                                                                                                               56, 25,
                                                                                                               23)
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][2]['supported']
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][2]['native']
        assert not parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][2]['many']
        assert parsed_dict['payment']['attributes'][14]['value']['user']['attributes'][2]['data_type'] == 'datetime'
        assert parsed_dict['payment']['attributes'][14]['supported']
        assert not parsed_dict['payment']['attributes'][14]['native']
        assert not parsed_dict['payment']['attributes'][14]['many']
        assert parsed_dict['payment']['attributes'][14]['data_type'] == 'User'


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
    prefix = 'camel_case'
    parsed_dict = parse_dict(camel_case_dict)
    quick_write(parsed_dict, f'{prefix}_parsed.json')

    model_list = transform_dict_to_model_list(parsed_dict)
    model_list = parse_for_patterns(model_list, PATTERN_FUNCTIONS)
    kmodel_list = build_serializer_data(model_list)

    quick_write(model_list, f'{prefix}_model_list.json')

    template_model_list = build_serializer_template_data(model_list)
    quick_write(template_model_list, f'{prefix}_serializer_template_data.json')

    writer = ReportWriter()
    output_file = output_folder / f'{prefix}_serializers_camel_case.py'
    writer.write('drf_serializers.py.j2', output_file, template_data=template_model_list)
    assert output_file.exists()


def test_attributes_with_list(output_folder, fixtures_folder):
    filename = fixtures_folder / 'api_bulk.json'
    with open(filename, 'r') as json_file:
        raw_data_dict = json.load(json_file)
    prefix = '_with_list'

    parsed_dict = parse_dict(raw_data_dict)
    quick_write(parsed_dict, f'{prefix}_parsed.json')

    model_list = transform_dict_to_model_list(parsed_dict)
    model_list = parse_for_patterns(model_list, PATTERN_FUNCTIONS)
    model_list = build_serializer_data(model_list)

    quick_write(model_list, f'{prefix}_model_list.json')

    template_model_list = build_serializer_template_data(model_list)
    quick_write(template_model_list, f'{prefix}_serializer_template_data.json')

    writer = ReportWriter()
    output_file = output_folder / f'{prefix}_serializers_camel_case.py'
    writer.write('drf_serializers.py.j2', output_file, template_data=template_model_list)
    assert output_file.exists()


def test_parsefile_for_ast_classes(fixtures_folder, output_folder):
    module_file = 'pydantic_models.py'
    filename = fixtures_folder / module_file

    ast_module = parse_file_for_ast_classes(filename)
    quick_write(ast_module, f'{module_file}.json')


class TestParseVarName:

    def test_parse_camel_case(self):
        varname = 'mySpecialVariable'
        snake_case_varname, was_changed = parse_var_name(varname)
        assert snake_case_varname == 'my_special_variable'
        assert was_changed

    def test_parse_pascal_case(self):
        varname = 'PaymentSerializer'
        snake_case_varname, was_changed = parse_var_name(varname)
        assert snake_case_varname == 'payment_serializer'
        assert was_changed

    def test_parse_snake_case(self):
        varname = 'flow_id'
        snake_case_varname, was_changed = parse_var_name(varname)
        assert snake_case_varname == 'flow_id'
        assert not was_changed

    @pytest.mark.parametrize('varname, expected',
                             [('IMEIValue', 'imei_value'),
                              ('DGINumberId', 'dgi_number_id')])
    def test_parse_with_acronym(self, varname, expected):
        snake_case_varname, was_changed = parse_var_name(varname)
        assert snake_case_varname == expected
        assert was_changed


def test_to_camel_case():
    data = {
        "amount": 100,
        "payer": {
            "fullName": "Nichole Stevens",
            "email": "ljones@example.org",
            "document": "07323861808"
        },
        "merchant_id": "something",
        "phone_number": "56985845"
    }
    dict_camelized = humps.camelize(data)
    # quick_write(dict_camelized, 'camelized_dict.json')
    assert dict_camelized['merchantId'] == data['merchant_id']
    assert dict_camelized['phoneNumber'] == data['phone_number']
    assert dict_camelized['payer']['fullName'] == data['payer']['fullName']
