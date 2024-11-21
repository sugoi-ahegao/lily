from typing import Any, Optional

from lily.models.user_settings.user_settings import UserSettings
from tests.testing_utils.generic import generic


def create_user_settings(
    template_file_dir: Optional[str] = None,
    template_file_name: Optional[str] = None,
    max_path_length: Optional[int] = None,
    field_removal_order: Optional[list[str]] = None,
    duplicate_suffix_template: Optional[str] = None,
) -> UserSettings:
    user_settings_dict: dict[Any, Any] = {
        "rename_rules": [
            {
                "template_file_dir": template_file_dir or generic.path.project_dir(),
                "template_file_name": template_file_name or "${title}",
                "post_templating_settings": {
                    "path": {
                        "max_path_length": max_path_length,
                        "field_removal_order": field_removal_order,
                        "duplicate_suffix_template": duplicate_suffix_template,
                    }
                },
            }
        ]
    }

    # For any none values, remove them so that the model uses its own defaults
    remove_none_values_from_dict(user_settings_dict)

    return UserSettings.model_validate(user_settings_dict)


def remove_none_values_from_dict(input_dict: dict[Any, Any]):
    """
    Recursively remove any keys with a value of None from a (nested) dict in-place.

    This is useful for removing optional values from a UserSettings dict before
    validating it with a pydantic model.

    Args:
        input_dict (dict[Any, Any]): The dict to remove None values from.

    Returns:
        None
    """
    for key, value in list(input_dict.items()):
        # iterate over each item in the list, check if it is a dict, then call recursively
        if isinstance(value, list):
            for item in value:  # type: ignore
                if isinstance(item, dict):
                    remove_none_values_from_dict(item)  # type: ignore

        # if it is a dict, call recursively
        if isinstance(value, dict):
            remove_none_values_from_dict(value)  # type: ignore

        # if the value is None, remove the key
        if value is None:
            del input_dict[key]

    return
