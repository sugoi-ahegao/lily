from pathlib import Path
from string import Template
from typing import Any

import yaml


def load_yaml_file(yaml_file_path: Path, replace: dict[str, str] | None = None) -> dict[Any, Any]:
    if replace is None:
        replace = {}

    with open(yaml_file_path, "r", encoding="utf-8") as f:
        file_as_string = Template(f.read()).safe_substitute(replace)

        return yaml.safe_load(file_as_string)
