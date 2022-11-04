import os
import sys
from pathlib import Path

import click

from django_scaffolding_tools.django.writers import write_model_serializer_from_models_file


@click.command()
@click.argument('command')
@click.option('--folder', default=os.getcwd())
@click.option('--model-file', default='models.py')
@click.option('--output-folder', default=None)
@click.option('--output-file', default=None)
@click.option('--camel-case', is_flag=True, default=False)
def main(command, folder, model_file, output_folder, output_file, camel_case):
    """Console script for django_scaffolding_tools."""
    click.echo(f"Current directory {os.getcwd()}")
    if command.lower() == 'model_2_serializer':
        click.echo(f'folder: {folder}')
        model_full_path = Path(folder) / model_file
        click.echo(f'model_file: {model_file} exists {model_full_path.exists()}')
        output_folder = Path(output_folder)
        click.echo(f'output_folder: {output_folder} exists: {output_folder}')
        if output_file is None:
            output_file = output_folder / f'{command}.py'
        click.echo(f'output_file: {output_file}')
        write_model_serializer_from_models_file(model_full_path, output_file, camel_case=camel_case)



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
