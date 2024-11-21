import json
from typing import Any, Literal

from lily.lily_logging.lily_logger import get_lily_logger
from lily.models.core import BaseModelWithExactAttributes
from lily.models.user_settings.rename_rule import RenameRule
from lily.utils.deep_merge import deep_merge_dicts
from pydantic import ValidationError


class UserSettings(BaseModelWithExactAttributes):
    version: Literal["0.0.1"]
    rename_rules: list[RenameRule]


def merge_global_rule_settings_with_all_rules(user_settings_dict: dict[Any, Any]) -> dict[Any, Any]:
    global_rule_settings = user_settings_dict.get("global_rule_settings")

    if global_rule_settings is None:
        return user_settings_dict

    for rule in user_settings_dict["rename_rules"]:
        deep_merge_dicts(rule, global_rule_settings)

    del user_settings_dict["global_rule_settings"]

    return user_settings_dict


def load_user_settings(user_settings_dict: dict[Any, Any]) -> UserSettings:
    logger = get_lily_logger()

    try:
        logger.debug(f"Obtained user settings as dict: {json.dumps(user_settings_dict)}")
        user_settings_dict = merge_global_rule_settings_with_all_rules(user_settings_dict)
        logger.debug(f"User settings with global rules merged as dict: {json.dumps(user_settings_dict)}")

        return UserSettings.model_validate(user_settings_dict)
    except ValidationError as e:
        raise ValueError(f"Failed to load user settings: {e}")
