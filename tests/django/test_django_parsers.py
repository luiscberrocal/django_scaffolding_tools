from django_scaffolding_tools.django.parsers import parse_for_django_classes
from django_scaffolding_tools.parsers import parse_file_for_ast_classes
from django_scaffolding_tools.utils.assert_utils import generate_pytest_assertions
from django_scaffolding_tools.utils.core import quick_write


def test_class_list(fixtures_folder, output_folder):
    module_file = 'models_with_helptext.py'
    filename = fixtures_folder / module_file

    ast_module = parse_file_for_ast_classes(filename)
    # quick_write(ast_module, f'ast_{module_file}.json', output_subfolder='django')

    django_classes = parse_for_django_classes(ast_module)
    # generate_pytest_assertions(django_classes, 'django_classes')
    # quick_write(django_classes, f'classes_{module_file}.json', output_subfolder='django')

    assert django_classes['classes'][0]['name'] == 'Payer'
    attrs_0 = django_classes['classes'][0]['attributes']
    assert attrs_0[0]['name'] == 'name'
    assert attrs_0[0]['keywords'][0]['name'] == 'max_length'
    assert attrs_0[0]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert attrs_0[0]['keywords'][0]['value'] == 100
    assert attrs_0[0]['data_type'] == 'CharField'
    assert attrs_0[1]['name'] == 'email'
    assert attrs_0[1]['keywords'][0]['name'] == 'max_length'
    assert attrs_0[1]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert attrs_0[1]['keywords'][0]['value'] == 100
    assert attrs_0[1]['data_type'] == 'CharField'
    assert attrs_0[2]['name'] == 'document'
    assert attrs_0[2]['keywords'][0]['name'] == 'max_length'
    assert attrs_0[2]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert attrs_0[2]['keywords'][0]['value'] == 100
    assert attrs_0[2]['keywords'][1]['name'] == 'help_text'
    assert attrs_0[2]['keywords'][1]['value_type_TMP'] == 'Call'
    assert attrs_0[2]['keywords'][1]['value'] == 'User’s personal identification number. To see the document ' \
                                                 'code list per country, go to the Country Reference page.'
    assert attrs_0[2]['data_type'] == 'CharField'
    assert attrs_0[3]['name'] == 'country'
    assert attrs_0[3]['keywords'][0]['name'] == 'max_length'
    assert attrs_0[3]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert attrs_0[3]['keywords'][0]['value'] == 2
    assert attrs_0[3]['keywords'][1]['name'] == 'help_text'
    assert attrs_0[3]['keywords'][1]['value_type_TMP'] == 'Call'
    assert attrs_0[3]['keywords'][1][
               'value'] == 'This will contain the two letter country code of the country the device was sold in.'
    assert attrs_0[3]['data_type'] == 'CharField'

    assert django_classes['classes'][1]['name'] == 'Payment'
    assert django_classes['classes'][1]['attributes'][0]['name'] == 'payer'
    assert django_classes['classes'][1]['attributes'][0]['keywords'][0]['name'] == 'verbose_name'
    assert django_classes['classes'][1]['attributes'][0]['keywords'][0]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][0]['keywords'][0][
               'value'] == 'This will contain the two letter country code of the country the device was sold in.'
    assert django_classes['classes'][1]['attributes'][0]['keywords'][1]['name'] == 'on_delete'
    assert django_classes['classes'][1]['attributes'][0]['keywords'][1]['value_type_TMP'] == 'Attribute'
    assert django_classes['classes'][1]['attributes'][0]['keywords'][1]['value'] == 'PROTECT'
    assert django_classes['classes'][1]['attributes'][0]['keywords'][2]['name'] == 'related_name'
    assert django_classes['classes'][1]['attributes'][0]['keywords'][2]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][0]['keywords'][2]['value'] == 'payments'
    assert django_classes['classes'][1]['attributes'][0]['data_type'] == 'ForeignKey'
    assert django_classes['classes'][1]['attributes'][1]['name'] == 'credit_line_id'
    assert django_classes['classes'][1]['attributes'][1]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][1]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][1]['keywords'][0]['value'] == 64
    assert django_classes['classes'][1]['attributes'][1]['keywords'][1]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][1]['keywords'][1]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][1]['keywords'][1][
               'value'] == 'Unique identifier for a credit line or a finance order.'
    assert django_classes['classes'][1]['attributes'][1]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][2]['name'] == 'finance_engine_version'
    assert django_classes['classes'][1]['attributes'][2]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][2]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][2]['keywords'][0]['value'] == 5
    assert django_classes['classes'][1]['attributes'][2]['keywords'][1]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][2]['keywords'][1]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][2]['keywords'][1][
               'value'] == 'Finance engine version FEv1 or FEv2'
    assert django_classes['classes'][1]['attributes'][2]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][3]['name'] == 'user_id'
    assert django_classes['classes'][1]['attributes'][3]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][3]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][3]['keywords'][0]['value'] == 50
    assert django_classes['classes'][1]['attributes'][3]['keywords'][1]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][3]['keywords'][1]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][3]['keywords'][1][
               'value'] == 'This will contain the foreign key to the Users table in M2 or the Persons table in M3'
    assert django_classes['classes'][1]['attributes'][3]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][4]['name'] == 'device_id'
    assert django_classes['classes'][1]['attributes'][4]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][4]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][4]['keywords'][0]['value'] == 50
    assert django_classes['classes'][1]['attributes'][4]['keywords'][1]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][4]['keywords'][1]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][4]['keywords'][1][
               'value'] == 'This will contain the foreign key to the Devices table'
    assert django_classes['classes'][1]['attributes'][4]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][5]['name'] == 'merchant_id'
    assert django_classes['classes'][1]['attributes'][5]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][5]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][5]['keywords'][0]['value'] == 64
    assert django_classes['classes'][1]['attributes'][5]['keywords'][1]['name'] == 'null'
    assert django_classes['classes'][1]['attributes'][5]['keywords'][1]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][5]['keywords'][1]['value']
    assert django_classes['classes'][1]['attributes'][5]['keywords'][2]['name'] == 'blank'
    assert django_classes['classes'][1]['attributes'][5]['keywords'][2]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][5]['keywords'][2]['value']
    assert django_classes['classes'][1]['attributes'][5]['keywords'][3]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][5]['keywords'][3]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][5]['keywords'][3][
               'value'] == 'Reference to the Merchants table - ONLY FEv2 needs to publish this information'
    assert django_classes['classes'][1]['attributes'][5]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][6]['name'] == 'clerk_id'
    assert django_classes['classes'][1]['attributes'][6]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][6]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][6]['keywords'][0]['value'] == 50
    assert django_classes['classes'][1]['attributes'][6]['keywords'][1]['name'] == 'null'
    assert django_classes['classes'][1]['attributes'][6]['keywords'][1]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][6]['keywords'][1]['value']
    assert django_classes['classes'][1]['attributes'][6]['keywords'][2]['name'] == 'blank'
    assert django_classes['classes'][1]['attributes'][6]['keywords'][2]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][6]['keywords'][2]['value']
    assert django_classes['classes'][1]['attributes'][6]['keywords'][3]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][6]['keywords'][3]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][6]['keywords'][3][
               'value'] == 'This will contain the foreign key to the clerk who sold the device'
    assert django_classes['classes'][1]['attributes'][6]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][7]['name'] == 'finance_provider'
    assert django_classes['classes'][1]['attributes'][7]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][7]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][7]['keywords'][0]['value'] == 50
    assert django_classes['classes'][1]['attributes'][7]['keywords'][1]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][7]['keywords'][1]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][7]['keywords'][1][
               'value'] == 'Constants representing the finance provider.'
    assert django_classes['classes'][1]['attributes'][7]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][8]['name'] == 'payment_provider'
    assert django_classes['classes'][1]['attributes'][8]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][8]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][8]['keywords'][0]['value'] == 16
    assert django_classes['classes'][1]['attributes'][8]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][9]['name'] == 'amount'
    assert django_classes['classes'][1]['attributes'][9]['keywords'][0]['name'] == 'max_digits'
    assert django_classes['classes'][1]['attributes'][9]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][9]['keywords'][0]['value'] == 12
    assert django_classes['classes'][1]['attributes'][9]['keywords'][1]['name'] == 'decimal_places'
    assert django_classes['classes'][1]['attributes'][9]['keywords'][1]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][9]['keywords'][1]['value'] == 2
    assert django_classes['classes'][1]['attributes'][9]['data_type'] == 'DecimalField'
    assert django_classes['classes'][1]['attributes'][10]['name'] == 'currency'
    assert django_classes['classes'][1]['attributes'][10]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][10]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][10]['keywords'][0]['value'] == 3
    assert django_classes['classes'][1]['attributes'][10]['keywords'][1]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][10]['keywords'][1]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][10]['keywords'][1][
               'value'] == 'The three letter currency code abbreviation.'
    assert django_classes['classes'][1]['attributes'][10]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][11]['name'] == 'country'
    assert django_classes['classes'][1]['attributes'][11]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][11]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][11]['keywords'][0]['value'] == 2
    assert django_classes['classes'][1]['attributes'][11]['keywords'][1]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][11]['keywords'][1]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][11]['keywords'][1][
               'value'] == 'This will contain the two letter country code of the country the device was sold in.'
    assert django_classes['classes'][1]['attributes'][11]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][12]['name'] == 'payment_method_id'
    assert django_classes['classes'][1]['attributes'][12]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][12]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][12]['keywords'][0]['value'] == 3
    assert django_classes['classes'][1]['attributes'][12]['keywords'][1]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][12]['keywords'][1]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][12]['keywords'][1][
               'value'] == 'Payment method defined by D-Local.'
    assert django_classes['classes'][1]['attributes'][12]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][13]['name'] == 'payment_method_flow'
    assert django_classes['classes'][1]['attributes'][13]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][13]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][13]['keywords'][0]['value'] == 15
    assert django_classes['classes'][1]['attributes'][13]['keywords'][1]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][13]['keywords'][1]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][13]['keywords'][1][
               'value'] == 'D-Local payment flow usually DIRECT or REDIRECT.'
    assert django_classes['classes'][1]['attributes'][13]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][14]['name'] == 'order_id'
    assert django_classes['classes'][1]['attributes'][14]['keywords'][0]['name'] == 'primary_key'
    assert django_classes['classes'][1]['attributes'][14]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert not django_classes['classes'][1]['attributes'][14]['keywords'][0]['value']
    assert django_classes['classes'][1]['attributes'][14]['keywords'][1]['name'] == 'unique'
    assert django_classes['classes'][1]['attributes'][14]['keywords'][1]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][14]['keywords'][1]['value']
    assert django_classes['classes'][1]['attributes'][14]['keywords'][2]['name'] == 'default'
    assert django_classes['classes'][1]['attributes'][14]['keywords'][2]['value_type_TMP'] == 'Attribute'
    assert django_classes['classes'][1]['attributes'][14]['keywords'][2]['value'] == 'uuid4'
    assert django_classes['classes'][1]['attributes'][14]['keywords'][3]['name'] == 'editable'
    assert django_classes['classes'][1]['attributes'][14]['keywords'][3]['value_type_TMP'] == 'Constant'
    assert not django_classes['classes'][1]['attributes'][14]['keywords'][3]['value']
    assert django_classes['classes'][1]['attributes'][14]['data_type'] == 'UUIDField'
    assert django_classes['classes'][1]['attributes'][15]['name'] == 'notification_url'
    assert django_classes['classes'][1]['attributes'][15]['data_type'] == 'URLField'
    assert django_classes['classes'][1]['attributes'][16]['name'] == 'payment_status'
    assert django_classes['classes'][1]['attributes'][16]['keywords'][0]['name'] == 'max_length'
    assert django_classes['classes'][1]['attributes'][16]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][16]['keywords'][0]['value'] == 15
    assert django_classes['classes'][1]['attributes'][16]['keywords'][1]['name'] == 'null'
    assert django_classes['classes'][1]['attributes'][16]['keywords'][1]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][16]['keywords'][1]['value']
    assert django_classes['classes'][1]['attributes'][16]['keywords'][2]['name'] == 'blank'
    assert django_classes['classes'][1]['attributes'][16]['keywords'][2]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][16]['keywords'][2]['value']
    assert django_classes['classes'][1]['attributes'][16]['keywords'][3]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][16]['keywords'][3]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][16]['keywords'][3][
               'value'] == 'The values should match pj_d_local_sdk.enums.PaymentStatus values.'
    assert django_classes['classes'][1]['attributes'][16]['data_type'] == 'CharField'
    assert django_classes['classes'][1]['attributes'][17]['name'] == 'response'
    assert django_classes['classes'][1]['attributes'][17]['keywords'][0]['name'] == 'default'
    assert django_classes['classes'][1]['attributes'][17]['keywords'][0]['value_type_TMP'] == 'Name'
    assert django_classes['classes'][1]['attributes'][17]['keywords'][0]['value'] == 'get_response_default_dict'
    assert django_classes['classes'][1]['attributes'][17]['keywords'][1]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][17]['keywords'][1]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][17]['keywords'][1][
               'value'] == 'Response from D-Local API. Will contain 2 keys for request response and callback response'
    assert django_classes['classes'][1]['attributes'][17]['data_type'] == 'JSONField'
    assert django_classes['classes'][1]['attributes'][18]['name'] == 'state'
    assert django_classes['classes'][1]['attributes'][18]['keywords'][0]['name'] == 'protected'
    assert django_classes['classes'][1]['attributes'][18]['keywords'][0]['value_type_TMP'] == 'Constant'
    assert django_classes['classes'][1]['attributes'][18]['keywords'][0]['value']
    assert django_classes['classes'][1]['attributes'][18]['keywords'][1]['name'] == 'default'
    assert django_classes['classes'][1]['attributes'][18]['keywords'][1]['value_type_TMP'] == 'Attribute'
    assert django_classes['classes'][1]['attributes'][18]['keywords'][1]['value'] == 'CREATED'
    assert django_classes['classes'][1]['attributes'][18]['data_type'] == 'FSMField'
    assert django_classes['classes'][1]['attributes'][19]['name'] == 'metadata'
    assert django_classes['classes'][1]['attributes'][19]['keywords'][0]['name'] == 'default'
    assert django_classes['classes'][1]['attributes'][19]['keywords'][0]['value_type_TMP'] == 'Name'
    assert django_classes['classes'][1]['attributes'][19]['keywords'][0]['value'] == 'get_metadata_default_dict'
    assert django_classes['classes'][1]['attributes'][19]['keywords'][1]['name'] == 'help_text'
    assert django_classes['classes'][1]['attributes'][19]['keywords'][1]['value_type_TMP'] == 'Call'
    assert django_classes['classes'][1]['attributes'][19]['keywords'][1][
               'value'] == 'Metadata for the payment. It includes the dates with the changes of state.'
    assert django_classes['classes'][1]['attributes'][19]['data_type'] == 'JSONField'
