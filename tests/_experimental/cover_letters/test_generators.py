from datetime import datetime
from pathlib import Path

from django_scaffolding_tools._experimental.cover_letters.config import ConfigurationManager
from django_scaffolding_tools._experimental.cover_letters.generators import convert_docx_to_pdf, write_docx_cover_letter


def test_write_cover_letter(fixtures_folder, output_folder):
    template = fixtures_folder / "_experimental" / "Cover Letter Template.docx"
    today = datetime.today()
    context = {"date": today.strftime("%b %M %Y"), "position_name": "Jedi Knight", "company_name": "Jedi Order Council"}

    docx_filename = f'{today.strftime("%Y%m%d")}_cover_{context["company_name"]}_{context["position_name"]}.docx'
    cover_letter = output_folder / docx_filename
    cover_letter.unlink(missing_ok=True)

    write_docx_cover_letter(template, context, cover_letter)
    assert cover_letter.exists()


def test_convert_docx_to_pdf(fixtures_folder, output_folder):
    config = ConfigurationManager()
    configuration = config.get_configuration()
    template = (
        Path(configuration["cover_letters"]["template_folder"]) / configuration["cover_letters"]["default_template"]
    )
    # template = fixtures_folder / '_experimental' / 'Cover Letter Template.docx'
    today = datetime.today()
    context = {
        "date": today.strftime("%B %-d, %Y"),
        "position_name": "Jedi Knight",
        "company_name": "Jedi Order Council",
    }
    naming_context = context  # humps.camelize(context)
    docx_filename = (
        f'{today.strftime("%Y%m%d")}_cover_{naming_context["company_name"]}' f'_{naming_context["position_name"]}.docx'
    )
    cover_letter = output_folder / docx_filename
    cover_letter.unlink(missing_ok=True)

    write_docx_cover_letter(template, context, cover_letter)
    assert cover_letter.exists()

    pdf = convert_docx_to_pdf(cover_letter, output_folder)
