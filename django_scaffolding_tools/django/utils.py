from typing import Dict, Any

from django_scaffolding_tools.exceptions import DjangoParsingException


def get_max_length(field_data: Dict[str, Any]) -> int:
    if field_data['data_type'] != 'CharField':
        raise DjangoParsingException('Max length can only be used for CharField.')
    for keyword in field_data['keywords']:
        if keyword.get('max_length') is not None:
            return keyword['value']
    raise DjangoParsingException('No max length keyword found.')
