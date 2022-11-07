from pathlib import Path
from typing import Dict, Any

from docxtpl import DocxTemplate


def write_cover_letter(template_file: Path, context: Dict[str, Any], output_file:Path):
    # Open our master template
    doc = DocxTemplate(template_file)
    # Load them up
    doc.render(context)
    # Save the file with personalized filename
    doc.save(output_file)

