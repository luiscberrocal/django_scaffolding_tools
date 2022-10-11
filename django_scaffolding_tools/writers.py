from pathlib import Path
from typing import Any, Dict, List

import jinja2


class ReportWriter:

    def __init__(self, template_path: Path, ):
        template_loader = jinja2.FileSystemLoader(searchpath=template_path)
        self.template_env = jinja2.Environment(loader=template_loader)

    def write(self, template_name: str, output_file: Path, **params):
        template = self.template_env.get_template(template_name)
        output = template.render(**params)
        with open(output_file, 'w') as html_file:
            html_file.write(output)


def write_serializer(model_list: List[Dict[str, Any]], output):
    writer = ReportWriter('./')

