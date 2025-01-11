import json
from pathlib import Path
from typing import Any, Dict, List, Union


def quick_json_write(
    data: Union[Dict[str, Any], List[Dict[str, Any]]], file: str, output_folder: Path, over_write: bool = True
):
    def quick_serialize(value):
        return f"{value}"

    filename = output_folder / file

    if (filename.exists() and over_write) or not filename.exists():
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4, default=quick_serialize)
        return filename


def quick_write(
    data: Union[Dict[str, Any], List[Dict[str, Any]]], file: str, output_subfolder: str = None, over_write: bool = True
):
    output_folder = Path(__file__).parent.parent.parent / "output"
    if not output_folder.exists():
        raise Exception(f"Output folder not found {output_folder}")
    if output_subfolder is None:
        folder = output_folder
    else:
        folder = output_folder / output_subfolder
    filename = quick_json_write(data, file, folder, over_write=over_write)
    return filename
