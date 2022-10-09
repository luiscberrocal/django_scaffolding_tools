import re
from operator import itemgetter
from typing import Dict, Any, List, Callable

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


def parse_dict(data: Dict[str, Any], model_name: str = 'Model', level: int = 0) -> Dict[str, Any]:
    parsed_dict: dict[str, dict[Any, Any] | list[Any]] = dict()
    key_name = to_snake_case(model_name)
    parsed_dict[key_name] = dict()
    parsed_dict[key_name]['name'] = model_name
    parsed_dict[key_name]['level'] = level
    parsed_dict[key_name]['attributes'] = list()
    for key, item in data.items():
        item_data = {'name': key, 'value': item, 'supported': False, 'native': True}
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


def build_serializer_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    pass
