from datetime import datetime, date

from django_scaffolding_tools.utils.assert_utils import generate_assertion_tuples


def test_generate_assert_dict():
    data_dict = {'name': 'Bruce', 'date_of_birth': datetime(1966, 5, 5, 13, 15, 0),
                 'pets': [{'type': 'dog', 'name': 'Nanook', 'dob': date(2019, 8, 5)}],
                 'address': {'street': 'First street', 'zip_code': '999999', 'super_hero': True, 'power': 7}}
    # data_dict = {'name': 'Bruce'}
    assert_list = generate_assertion_tuples(data_dict, 'data_dict')
    for assertion_tuple in assert_list:
        print(f'{assertion_tuple.var_name} == {assertion_tuple.value}')
