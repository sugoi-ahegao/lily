from collections.abc import Mapping
from typing import Any


def deep_merge_dicts(dictA: dict[Any, Any], dictB: dict[Any, Any]):
    merged = dictA  # Start with a copy of dict1 to avoid modifying it

    for key, value in dictB.items():
        if key in merged and isinstance(merged[key], Mapping) and isinstance(value, Mapping):
            # Recursively merge nested dictionaries
            merged[key] = deep_merge_dicts(merged[key], value)  # type: ignore
        else:
            # Overwrite or add the value
            merged[key] = value

    return merged
