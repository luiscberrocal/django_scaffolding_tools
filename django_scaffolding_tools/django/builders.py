from typing import Any, Dict, List

import humps


def build_model_serializer_template_data(parsed_django_classes: Dict[str, Any], add_source_camel_case=False) -> List[Dict[str, Any]]:
    template_data = list()

    for model in parsed_django_classes['classes']:
        serializer_data = dict()
        serializer_data['name'] = f'{model["name"]}Serializer(serializers.ModelSerializer)'
        serializer_data['model'] = model['name']
        serializer_data['fields'] = list()
        for attribute in model['attributes']:
            serializer_attribute = dict()
            serializer_attribute['name'] = attribute['name']
            if add_source_camel_case:
                source = humps.camelize(attribute['name'])
                if source != attribute['name']:
                    serializer_attribute['source'] = source
            serializer_data['fields'].append(serializer_attribute)
        template_data.append(serializer_data)

    return template_data
