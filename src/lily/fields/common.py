import operator
import re
from typing import Any, Optional

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


OPERATORS: dict[str, Any] = {
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq,
    "!=": operator.ne,
}


def satisfies_all_constraints(value: float, constraints_as_str: str) -> bool:
    return all([satisfies_constraint(value, constraint_str) for constraint_str in constraints_as_str.split(",")])


def satisfies_constraint(value: float, constraint_str: str) -> bool:
    match = re.match(r"(>=|<=|>|<|==|!=)\s*(-?\d+(\.\d+)?)", constraint_str.strip())

    if not match:
        raise ValueError(f"Invalid constraint format: {constraint_str}")

    op, num = match.group(1), float(match.group(2))

    return OPERATORS[op](value, num)
