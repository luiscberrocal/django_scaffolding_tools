from typing import Any, Dict, List

import humps


def build_model_serializer_template_data(parsed_django_classes: Dict[str, Any],
                                         add_source_camel_case=False) -> Dict[str, Any]:
    template_data = {'classes': list(), 'imports': ['from rest_framework import serializers']}
    for model in parsed_django_classes['classes']:
        serializer_data = dict()
        serializer_data['name'] = f'{model["name"]}Serializer(serializers.ModelSerializer)'
        serializer_data['model'] = model['name']
        serializer_data['fields'] = list()
        for attribute in model['attributes']:
            serializer_attribute = dict()
            serializer_attribute['name'] = attribute['name']
            serializer_attribute['add_field'] = False
            keywords = dict()
            if add_source_camel_case:
                source = humps.camelize(attribute['name'])
                if source != attribute['name']:
                    serializer_attribute['source'] = source
                    keywords['source'] = source
                    serializer_attribute['add_field'] = True
            keyword_content = ''
            keyword_content_str = ''
            for keyword, value in keywords.items():
                keyword_content += f'{keyword}=\'{value}\', '
            if len(keyword_content) > 0:
                keyword_content_str = keyword_content[:-2]
            serializer_attribute['serializer'] = f'serializers.{attribute["data_type"]}({keyword_content_str})'
            if attribute['data_type'] == 'ForeignKey':
                keyword_content += 'read_only=True, '
                keyword_content_str = keyword_content[:-2]
                classname = attribute["arguments"][0]["value"]
                serializer_attribute['serializer'] = f'{classname}Serializer({keyword_content_str})'
                serializer_attribute['add_field'] = True

            serializer_data['fields'].append(serializer_attribute)
        template_data['classes'].append(serializer_data)

    return template_data
