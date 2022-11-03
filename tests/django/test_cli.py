from click.testing import CliRunner

from django_scaffolding_tools.django import cli


def test_model_2_serializer(output_folder, fixtures_folder):
    out_file = output_folder / 'serializers.py'
    out_file.unlink(missing_ok=True)

    runner = CliRunner()
    commands = ['model_2_serializer', '--folder', fixtures_folder, '--output-folder', output_folder]
    help_result = runner.invoke(cli.main, commands)
    print(help_result)

    assert help_result.exit_code == 0
