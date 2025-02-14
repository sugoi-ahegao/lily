import operator
import re
from typing import Any

from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext

OPERATORS: dict[str, Any] = {
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq,
    "!=": operator.ne,
}


class MatchesRatingFilterSettings(BaseModelWithExactAttributes):
    constraint: str


def matches_rating(stash_context: StashContext, settings: MatchesRatingFilterSettings):
    scene_rating = stash_context.scene.rating100

    if scene_rating is None:
        return False

    return satisfies_all_constraints(scene_rating, settings.constraint)


def satisfies_all_constraints(value: float, constraints_as_str: str) -> bool:
    return all([satisfies_constraint(value, constraint_str) for constraint_str in constraints_as_str.split(",")])


def satisfies_constraint(value: float, constraint_str: str) -> bool:
    match = re.match(r"(>=|<=|>|<|==|!=)\s*(-?\d+(\.\d+)?)", constraint_str.strip())

    if not match:
        raise ValueError(f"Invalid constraint format: {constraint_str}")

    op, num = match.group(1), float(match.group(2))

    return OPERATORS[op](value, num)
