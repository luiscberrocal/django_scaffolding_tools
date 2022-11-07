from datetime import datetime

from django_scaffolding_tools._experimental.cover_letters.generators import write_cover_letter


def test_write_cover_letter(fixtures_folder, output_folder):
    template = fixtures_folder / '_experimental' / 'Cover Letter Template.docx'
    today = datetime.today()
    context = {'today': today.strftime('%b %M %Y'), 'position_name': 'Jedi', 'company_name': 'Jedi Order'}

    cover_letter = output_folder / f'{today.strftime("%Y%m%d")}_cover_{context["company_name"]}_{context["position_name"]}.docx'
    cover_letter.unlink(missing_ok=True)

    write_cover_letter(template, context, cover_letter)
    assert cover_letter.exists()
