import json
from pathlib import Path

from jinja2 import PackageLoader, Environment

from django_scaffolding_tools.parsers import parse_dict, transform_dict_to_model_list, post_process_attributes, \
    build_serializer_data
from django_scaffolding_tools.patterns import PATTERN_FUNCTIONS


class ReportWriter:

    def __init__(self):
        self.template_env = Environment(loader=PackageLoader('django_scaffolding_tools', 'templates'))

    def write(self, template_name: str, output_file: Path, **params):
        template = self.template_env.get_template(template_name)
        output = template.render(**params)
        with open(output_file, 'w') as html_file:
            html_file.write(output)


def write_serializer_from_file(source_file: Path, output_file: Path):
    with open(source_file, 'r') as json_file:
        data = json.load(json_file)

    writer = ReportWriter()
    parsed_dict = parse_dict(data)

    model_list = transform_dict_to_model_list(parsed_dict)
    model_list = post_process_attributes(model_list, PATTERN_FUNCTIONS)
    model_list = build_serializer_data(model_list)

    writer.write('serializers.py.j2', output_file, model_list=model_list)
