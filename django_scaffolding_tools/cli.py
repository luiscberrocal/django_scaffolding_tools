"""Console script for django_scaffolding_tools."""

import logging
import os
import sys
from pathlib import Path
from platform import python_version

import click

from django_scaffolding_tools.django.cli import models_to_json
from django_scaffolding_tools.enums import CommandType
from django_scaffolding_tools.writers import write_serializer_from_file

from . import __version__ as current_version

logger = logging.getLogger(__name__)


@click.command()
@click.argument("command")
@click.option("--source-file")
@click.option("--output-folder")
def main2(command, source_file, output_folder):
    """Console script for django_scaffolding_tools."""
    click.echo(f"See click documentation {os.getcwd()}")
    if command == CommandType.JSON_TO_SERIALIZER:
        source_file_path = Path(source_file)
        output_folder = Path(output_folder)
        if output_folder.exists():
            target_file = output_folder / "__serializers.py"
            click.echo(f"JSON to serializer from {source_file_path} to {target_file}")
            try:
                write_serializer_from_file(source_file_path, target_file)
            except Exception as e:
                error_message = f"Type: {e.__class__.__name__} Error: {e}"
                print(error_message)
                return 200
            return 0
        print(f"NO output folder {output_folder}")
        raise Exception("No output folder")


@click.group()
@click.version_option(version=current_version)
def main():
    pass


@click.command()
def about():
    banner_char = "-"
    app_name = "Django Scaffolding Tools"
    length = len(app_name) + 4
    click.echo(banner_char * length)
    click.echo(f"{banner_char} {app_name} {banner_char}")
    click.echo(banner_char * length)
    click.echo(f"Operating System: {sys.platform}")
    click.echo(f"Python : {python_version()}")
    logger.debug("Ran about command.")


main.add_command(about)
main.add_command(models_to_json)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
