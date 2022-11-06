from typing import Dict, Any

from django_scaffolding_tools.enums import ASTDataType
from django_scaffolding_tools.exceptions import DjangoParsingException


def parse_for_django_classes(module: Dict[str, Any]) -> Dict[str, any]:
    module_content = dict()
    django_classes = list()
    module_content['classes'] = django_classes

    for content in module['body']:
        if content.get('_type') == ASTDataType.CLASS:
            model = dict()
            model['name'] = content.get('name')
            model['attributes'] = list()
            for class_content in content['body']:
                if class_content.get('_type') == ASTDataType.ASSIGN:
                    field = dict()
                    # Name of the field
                    field['name'] = class_content['targets'][0]['id']
                    field['keywords'] = list()
                    field['arguments'] = list()
                    try:
                        field['data_type'] = get_data_type(class_content)
                    except KeyError as e:
                        error_message = f'Key error {e}. Model {model["name"]} attr {field["name"]}'
                        raise DjangoParsingException(error_message)

                    if field['data_type'] == 'ForeignKey':
                        first_argument = class_content['value']['args'][0]
                        if first_argument.get('_type') == ASTDataType.ATTRIBUTE:
                            if first_argument.get('attr') == 'AUTH_USER_MODEL':
                                field['arguments'].append({'name': 'fk_classname', 'value': 'User'})
                        else:
                            fk_classname = first_argument['id']
                            field['arguments'].append({'name': 'fk_classname', 'value': fk_classname})
                    try:
                        for keyword in class_content['value']['keywords']:
                            keyword_data = dict()
                            keyword_data['name'] = keyword['arg']
                            value_type = keyword['value']['_type']
                            keyword_data['value_type_TMP'] = value_type

                            if value_type == ASTDataType.CONSTANT:
                                keyword_value = keyword['value'].get('value')
                            elif value_type == ASTDataType.NAME:
                                keyword_value = keyword['value'].get('id')
                            elif value_type == ASTDataType.ATTRIBUTE:
                                keyword_value = keyword['value'].get('attr')
                            elif value_type == ASTDataType.CALL and keyword_data['name'] == 'help_text':
                                if len(keyword['value'].get('args')) > 0:
                                    call_args_type = keyword['value']['args'][0]['_type']
                                    if call_args_type == ASTDataType.CONSTANT:
                                        keyword_value = keyword['value']['args'][0].get('value')

                            keyword_data['value'] = keyword_value
                            field['keywords'].append(keyword_data)
                    except KeyError:
                        print(f'Error with field {model["name"]}.{field["name"]}')
                    model['attributes'].append(field)
            django_classes.append(model)
    return module_content


def get_data_type(class_content):
    data_type = None
    if class_content['value']['_type'] == ASTDataType.CONSTANT:
        data_type = 'CONSTANT'
    elif class_content['value']['_type'] == ASTDataType.CALL:
        func_ = class_content['value']['func']
        data_type = func_.get('attr')
    elif class_content['value']['_type'] == ASTDataType.NAME:
        func_ = class_content['value']['func']
        data_type = func_.get('id')
    else:
        error_msg = f'Unsupported data type {class_content["value"]["_type"]}.'
        DjangoParsingException(error_msg)
    if data_type is None:
        data_type = 'UNSUPPORTED'
    return data_type
