#!/usr/bin/env python

"""Tests for `django_scaffolding_tools` package."""

import pytest
from click.testing import CliRunner

from django_scaffolding_tools import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'django_scaffolding_tools.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_cmd_json_to_ser(output_folder):
    out_file = output_folder / '__serializers.py'
    out_file.unlink(missing_ok=True)

    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['J2SER', '--source-file', './fixtures/json_data.json', '--output-folder',
                                           output_folder])

    assert help_result.exit_code == 0
    print(help_result.output)
    assert out_file.exists()
