from pathlib import Path

from django_scaffolding_tools.writers import write_serializer_from_file


def test_write_serializers(output_folder):
    source_filename = Path(__file__).parent / 'fixtures' / 'json_data.json'
    assert source_filename.exists()

    target_file = output_folder / 'test_write_serializers.py'
    write_serializer_from_file(source_filename, target_file)
