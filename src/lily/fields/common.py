import re
from typing import Optional

from lily.models.core import BaseModelWithExactAttributes


class TextReplacementSetting(BaseModelWithExactAttributes):
    find: str
    replace: str
    use_regex: bool = False


def apply_text_replacements(text: str, settings: Optional[list[TextReplacementSetting]]):
    if settings is None:
        return text

    for setting in settings:
        text = apply_text_replacement(text, setting.find, setting.replace, setting.use_regex)

    return text


def apply_text_replacement(text: str, find_pattern: str, replace_with: str, use_regex: bool = False):
    if use_regex:
        return re.sub(find_pattern, replace_with, text)

    return text.replace(find_pattern, replace_with)
