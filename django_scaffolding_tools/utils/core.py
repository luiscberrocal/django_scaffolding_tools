import json
from pathlib import Path
from typing import Union, Dict, Any, List


def quick_write(data: Union[Dict[str, Any], List[Dict[str, Any]]], file: str, output_subfolder: str = None,
                over_write: bool = True):
    def quick_serialize(value):
        return f'{value}'

    output_folder = Path(__file__).parent.parent / 'output'
    if output_subfolder is not None:
        folder = output_folder / output_subfolder
        folder.mkdir(exist_ok=True)
    else:
        folder = output_subfolder
    filename = folder / file

    if (filename.exists() and over_write) or not filename.exists():
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4, default=quick_serialize)
        return filename
