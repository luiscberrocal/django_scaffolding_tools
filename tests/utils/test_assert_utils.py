from datetime import datetime

from django_scaffolding_tools.utils.assert_utils import generate_dict_assertions


def test_generate_assert_dict():
    data_dict = {'name': 'Bruce', 'date_of_birth': datetime, 'pets': [{'type': 'dog'}],
                 'address': {'street': 'First street', 'zip_code': '999999'}}
    # data_dict = {'name': 'Bruce'}
    assert_list = generate_dict_assertions(data_dict, 'data_dict')
    print(assert_list)

