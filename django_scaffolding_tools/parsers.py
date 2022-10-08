import re
from typing import Dict, Any, List

import humps


def to_snake_case(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


def parse_dict(data: Dict[str, Any], model_name: str = 'Model') -> Dict[str, Any]:
    parsed_dict: dict[str, dict[Any, Any] | list[Any]] = dict()
    key_name = to_snake_case(model_name)
    parsed_dict[key_name] = dict()
    parsed_dict[key_name]['name'] = model_name
    parsed_dict[key_name]['attributes'] = list()
    for key, item in data.items():
        item_data = {'name': key, 'value': item, 'supported': False}
        if isinstance(item, str):
            item_data['type'] = 'str'
            item_data['length'] = len(item)
            item_data['supported'] = True
        elif isinstance(item, float):
            item_data['type'] = 'float'
            item_data['supported'] = True
        elif isinstance(item, int):
            item_data['type'] = 'int'
            item_data['supported'] = True
        elif isinstance(item, dict):
            item_data['type'] = 'object'
            item_data['value'] = parse_dict(item, model_name=humps.pascalize(key))
            item_data['supported'] = True
        else:
            item_data['type'] = item.__class__.__name__

        parsed_dict[key_name]['attributes'].append(item_data)
    return parsed_dict


def build_serializer_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    pass
