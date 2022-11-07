from datetime import datetime

import humps

from django_scaffolding_tools._experimental.cover_letters.generators import write_docx_cover_letter, convert_docx_to_pdf


def test_write_cover_letter(fixtures_folder, output_folder):
    template = fixtures_folder / '_experimental' / 'Cover Letter Template.docx'
    today = datetime.today()
    context = {'today': today.strftime('%b %M %Y'), 'position_name': 'Jedi Knight',
               'company_name': 'Jedi Order Council'}

    docx_filename = f'{today.strftime("%Y%m%d")}_cover_{context["company_name"]}_{context["position_name"]}.docx'
    cover_letter = output_folder / docx_filename
    cover_letter.unlink(missing_ok=True)

    write_docx_cover_letter(template, context, cover_letter)
    assert cover_letter.exists()


def test_convert_docx_to_pdf(fixtures_folder, output_folder):
    template = fixtures_folder / '_experimental' / 'Cover Letter Template.docx'
    today = datetime.today()
    context = {'today': today.strftime('%b %M %Y'), 'position_name': 'Jedi Knight',
               'company_name': 'Jedi Order Council'}
    naming_context = context  # humps.camelize(context)
    docx_filename = f'{today.strftime("%Y%m%d")}_cover_{naming_context["company_name"]}' \
                    f'_{naming_context["position_name"]}.docx'
    cover_letter = output_folder / docx_filename
    cover_letter.unlink(missing_ok=True)

    write_docx_cover_letter(template, context, cover_letter)
    assert cover_letter.exists()

    pdf = convert_docx_to_pdf(cover_letter, output_folder)
