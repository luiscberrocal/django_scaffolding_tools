from typing import Dict, Any, Tuple

from django_scaffolding_tools.exceptions import DjangoParsingException


def get_max_length(field_data: Dict[str, Any]) -> int:
    if field_data['data_type'] != 'CharField':
        raise DjangoParsingException('Max length can only be used for CharField.')
    for keyword in field_data['keywords']:
        if keyword.get('name') == 'max_length':
            return keyword['value']
    raise DjangoParsingException('No max length keyword found.')


def get_decimal_info(field_data: Dict[str, Any]) -> Tuple[int, int]:
    max_digits = 0
    decimal_places = 0
    if field_data['data_type'] != 'DecimalField':
        raise DjangoParsingException('Not a decimal field.')
    for keyword in field_data['keywords']:
        if keyword.get('name') == 'max_digits':
            max_digits = keyword['value']
        elif keyword.get('name') == 'decimal_places':
            decimal_places = keyword['value']
    return max_digits, decimal_places
