import ast
import csv
from pathlib import Path
from typing import Any, Dict

from ast2json import ast2json


def extract_field_info(field: Dict[str, Any]) -> Dict[str, str]:
    """Extracts the necessary information from a field in the AST."""
    if field["annotation"].get("id") is None:
        data_type = "UNKNOWN"
    else:
        data_type = field["annotation"]["id"]
    field_info = {"name": field["target"]["id"], "alias": "", "description": "", "example": "", "data_type": data_type}

    for keyword in field["value"]["keywords"]:
        if keyword["arg"] == "alias":
            field_info["alias"] = keyword["value"]["s"]
        elif keyword["arg"] == "description":
            field_info["description"] = keyword["value"]["s"]
        elif keyword["arg"] == "example":
            field_info["example"] = keyword["value"]["s"]

    return field_info


def generate_csv(filename: str, output_filename: str) -> None:
    """Generates a CSV file from a Python file containing a Pydantic model."""
    with open(filename) as py_file:
        content = py_file.read()

    node = ast.parse(content)
    node_dict = ast2json(node)
    # FIXME Delete this snippet
    import json
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    var_name = "node_dict"
    var_value = eval(var_name)
    filename = f"__{timestamp}_{var_name}__.json"
    with open(filename, "w") as f:
        json.dump(var_value, f, indent=4, default=str)
    print("Wrote variable to:", filename)
    ############################################################

    field_infos = []
    for class_def in node_dict["body"]:
        if class_def["_type"] == "ClassDef" and class_def["name"] == "StatusChangeEvent":
            for field in class_def["body"]:
                if field["_type"] == "AnnAssign":
                    field_info = extract_field_info(field)
                    field_infos.append(field_info)

    with open(output_filename, "w", newline="") as csv_file:
        fieldnames = ["name", "alias", "description", "example", "data_type"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for field_info in field_infos:
            writer.writerow(field_info)


# Usage

if __name__ == "__main__":
    f = Path(__file__).parent / "schemas.py"
    generate_csv(str(f), "StatusChangeEvent.csv")
