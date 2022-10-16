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
@click.option('--output-folder')
def main(command, source_file, output_folder):
    """Console script for django_scaffolding_tools."""
    click.echo(f"See click documentation {os.getcwd()}")
    if command == CommandType.JSON_TO_SERIALIZER:
        source_file_path = Path(source_file)
        output_folder = Path(output_folder)
        if output_folder.exists():
            target_file = output_folder / '__serializers.py'
            click.echo(f'JSON to serializer from {source_file_path} to {target_file}')
            try:
                write_serializer_from_file(source_file_path, target_file)
            except Exception as e:
                error_message = f'Type: {e.__class__.__name__} Error: {e}'
                print(error_message)
                return 200
            return 0
        else:
            print(f'NO output folder {output_folder}')
            raise Exception('No output folder')


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
