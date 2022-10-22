from typing import Any, List, Dict

from django_scaffolding_tools.enums import NativeDataType
from django_scaffolding_tools.parsers import SERIALIZER_FIELDS


def build_serializer_template_data(model_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Builds a dictionary to be used in the Jinja template"""
    template_data = dict()
    template_data['imports'] = ['from rest_framework import serializers']
    template_models = list()
    template_data['classes'] = template_models
    for model in model_list:
        serializer_data = dict()
        serializer_data['name'] = f'serializers.{model["name"]}Serializer(serializers.Serializer)'
        serializer_data['attributes'] = list()
        for attribute in model['attributes']:
            serializer_attribute = dict()
            serializer_attribute['name'] = attribute['name']
            keywords = list()
            for keyword in attribute['serializer'].get('keywords'):
                if isinstance(keyword['value'], str):
                    keywords.append(f'{keyword["name"]}=\'{keyword["value"]}\'')
                else:
                    keywords.append(f'{keyword["name"]}={keyword["value"]}')
            field_vars = ', '.join(keywords)
            serializer_attribute['field'] = f'serializers.{attribute["serializer"]["field_type"]}({field_vars})'
            serializer_data['attributes'].append(serializer_attribute)
        template_models.append(serializer_data)
    return template_data


def build_serializer_info(field_type: str, keywords: List[Dict[str, Any]]):
    field_data = {'field_type': field_type, 'keywords': keywords}
    return field_data


def build_serializer_data(model_list: List[Dict[str, Any]],
                          serializer_fields: Dict[str, Any] = SERIALIZER_FIELDS) -> List[Dict[str, Any]]:
    for model in model_list:
        for attribute in model['attributes']:
            data_type = attribute['data_type']
            keywords = list()
            if data_type == NativeDataType.STRING:
                pattern_type = attribute.get('pattern_type')
                keywords.append({'name': 'max_length', 'value': attribute['length']})
                if pattern_type is None:
                    serializer_field = serializer_fields.get(data_type)
                    if serializer_field is not None:
                        if attribute.get('alias'):
                            keywords.append({'name': 'source', 'value': attribute['alias']})
                    attribute['serializer'] = {'field_type': serializer_field['field'], 'keywords': keywords}
                else:
                    serializer_field = serializer_fields.get(pattern_type)
                    if attribute.get('alias'):
                        keywords.append({'name': 'source', 'value': attribute['alias']})
                    attribute['serializer'] = {'field_type': serializer_field['field'], 'keywords': keywords}
            else:
                serializer_field = serializer_fields.get(data_type)
                if attribute.get('alias'):
                    keywords.append({'name': 'source', 'value': attribute['alias']})
                if serializer_field is None:
                    attribute['serializer'] = {'field_type': f'{attribute["data_type"]}Serializer',
                                               'keywords': keywords}
                else:
                    attribute['serializer'] = {'field_type': serializer_field['field'], 'keywords': keywords}

    return model_list
