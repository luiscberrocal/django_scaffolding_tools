import re
from operator import itemgetter
from typing import Dict, Any, List, Callable, Tuple

import humps

from django_scaffolding_tools.enums import NativeDataType, PatternType


def to_snake_case(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


def transform_dict_to_model_list(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    model_list = list()
    for key, model in data.items():
        model_list.append(model)
        for att in model['attributes']:
            if not att['native']:
                model_list += transform_dict_to_model_list(att['value'])
    return sorted(model_list, key=itemgetter('level'), reverse=True)


def parse_var_name(var_name: str) -> Tuple[str, bool]:
    if humps.is_snakecase(var_name):
        new_var_name = var_name
    elif humps.is_camelcase(var_name):
        new_var_name = humps.decamelize(var_name)
    elif humps.is_pascalcase(var_name):
        new_var_name = humps.depascalize(var_name)
    else:
        raise Exception('Unsupported casing.')
    return new_var_name, new_var_name != var_name


def parse_dict(data: Dict[str, Any], model_name: str = 'Model', level: int = 0) -> Dict[str, Any]:
    parsed_dict: dict[str, dict[Any, Any] | list[Any]] = dict()
    key_name = to_snake_case(model_name)
    parsed_dict[key_name] = dict()
    parsed_dict[key_name]['name'] = model_name
    parsed_dict[key_name]['level'] = level
    parsed_dict[key_name]['attributes'] = list()
    for key, item in data.items():
        variable_name, add_alias = parse_var_name(key)

        item_data = {'name': variable_name, 'value': item, 'supported': False, 'native': True}
        if add_alias:
            item_data['alias'] = key
        data_type = item.__class__.__name__
        if data_type in NativeDataType.to_list():
            item_data['type'] = data_type
            item_data['supported'] = True
            if data_type == NativeDataType.STRING.value:
                item_data['length'] = len(item)
        elif isinstance(item, dict):
            pascalized_model_name = humps.pascalize(key)
            item_data['type'] = pascalized_model_name
            item_data['value'] = parse_dict(item, model_name=pascalized_model_name, level=level + 1)
            item_data['supported'] = True
            item_data['native'] = False
        else:
            item_data['type'] = data_type

        parsed_dict[key_name]['attributes'].append(item_data)
    return parsed_dict


def post_process_attributes(model_list: List[Dict[str, Any]],
                            pattern_functions: List[Callable[[str], PatternType]]) -> List[Dict[str, Any]]:
    for model in model_list:
        for attribute in model['attributes']:
            if attribute['type'] == NativeDataType.STRING:
                for pattern_function in pattern_functions:
                    pattern = pattern_function(attribute['value'])
                    if pattern is not None:
                        attribute['pattern_type'] = pattern
                        break
    return model_list


SERIALIZER_FIELDS = {
    NativeDataType.STRING: {'field': 'CharField'},
    NativeDataType.INTEGER: {'field': 'IntegerField'},
    NativeDataType.FLOAT: {'field': 'FloatField'},
    NativeDataType.DATE: {'field': 'DateField'},
    NativeDataType.DATETIME: {'field': 'DatetimeField'},
    PatternType.DATE: {'field': 'DateField'},
    PatternType.DATETIME: {'field': 'DatetimeField'},
    PatternType.URL: {'field': 'UrlField'},
    PatternType.EMAIL: {'field': 'EmailField'},
}


def build_serializer_data(model_list: List[Dict[str, Any]],
                          serializer_fields: Dict[str, Any] = SERIALIZER_FIELDS) -> List[Dict[str, Any]]:
    for model in model_list:
        for attribute in model['attributes']:
            data_type = attribute['type']
            source_data =''
            if data_type == NativeDataType.STRING:
                pattern_type = attribute.get('pattern_type')
                if pattern_type is None:
                    serializer_field = serializer_fields.get(data_type)
                    if serializer_field is not None:
                        if attribute.get('alias'):
                            source_data = f'source=\'{attribute["alias"]}\''
                            attribute['serializer'] = f'{serializer_field["field"]}(max_length=' \
                                                      f'{attribute["length"]}, {source_data})'
                        else:
                            attribute['serializer'] = f'{serializer_field["field"]}(max_length=' \
                                                      f'{attribute["length"]})'

                else:
                    serializer_field = serializer_fields.get(pattern_type)
                    if attribute.get('alias'):
                        source_data = f'source=\'{attribute["alias"]}\''
                    if serializer_field is not None:
                        attribute['serializer'] = f'{serializer_field["field"]}({source_data})'
            else:
                serializer_field = serializer_fields.get(data_type)
                if attribute.get('alias'):
                    source_data = f'source=\'{attribute["alias"]}\''
                if serializer_field is None:
                    attribute['serializer'] = f'{attribute["type"]}Serializer({source_data})'
                else:
                    attribute['serializer'] = f'{serializer_field["field"]}({source_data})'

    return model_list
