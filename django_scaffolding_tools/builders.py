from typing import Any, List, Dict


def build_serializer_template_data(model_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Builds a dictionary to be used in the Jinja template"""
    template_models = list()
    for model in model_list:
        serializer_data = dict()
        serializer_data['name'] = model['name']
        serializer_data['attributes'] = list()
        for attribute in serializer_data['attributes']:
            serializer_attribute = dict()
            serializer_attribute['name'] = attribute['name']
            keywords = list()
            for keyword in attribute['serializer'].get('keywords'):
                keywords.append(f'{keyword["name"]}={keyword["value"]}')
            field_vars = ', '.join(keyword)
            serializer_attribute['field'] = f'serializers.{attribute["serializer"]["field_type"]}({field_vars})'
            serializer_data['attributes'].append(serializer_attribute)
        template_models.append(serializer_data)
    return template_models
