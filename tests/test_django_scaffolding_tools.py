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


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'django_scaffolding_tools.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_cmd_json_to_ser():
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['J2SER', '--source-file', './fixtures/json_sample.json'])

    # assert help_result.exit_code == 0
    print(help_result.output)
