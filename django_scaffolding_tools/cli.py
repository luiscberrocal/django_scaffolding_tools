"""Console script for django_scaffolding_tools."""
import sys
from pathlib import Path

import click
import os

from django_scaffolding_tools.enums import CommandType
from django_scaffolding_tools.writers import write_serializer_from_file


@click.command()
@click.argument('command')
@click.option('--source-file')
def main(command, source_file):
    """Console script for django_scaffolding_tools."""
    click.echo(f"See click documentation {os.getcwd()}")
    if command == CommandType.JSON_TO_SERIALIZER:
        source_file_path = Path(source_file)
        current_folder = Path(os.getcwd() / 'output')
        if current_folder.exists():
            target_file = source_file_path.parent / '__serializers.py'
            click.echo(f'JSON to serializer from {source_file_path} to {target_file}')
            write_serializer_from_file(source_file_path, target_file)
            return 0
        else:
            raise Exception('No output folder')


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
