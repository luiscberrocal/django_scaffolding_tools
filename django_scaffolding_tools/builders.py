from typing import Any, List, Dict


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
