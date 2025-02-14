import operator
from enum import Enum
from typing import Optional

from lily.fields.common import TextReplacementSetting, apply_text_replacements
from lily.models.core import BaseModelWithExactAttributes
from lily.models.stash_graphql_models.performer import GenderEnum, Performer
from lily.stash_context import StashContext


class PerformerSortKey(str, Enum):
    ID = "id"
    NAME = "name"
    RATING = "rating"
    FAVORITE = "favorite"


class PerformerLimitExceededBehavior(str, Enum):
    KEEP = "keep"
    DISCARD = "discard"


class PerformerFieldSettings(BaseModelWithExactAttributes):
    separator: str = " "
    sort_by: list[PerformerSortKey] = [PerformerSortKey.ID]
    limit: Optional[int] = None
    limit_exceeded_behavior: PerformerLimitExceededBehavior = PerformerLimitExceededBehavior.KEEP
    exclude_genders: Optional[list[GenderEnum]] = None
    replacements: Optional[list[TextReplacementSetting]] = None


def performers_field(stash_context: StashContext, settings: PerformerFieldSettings) -> str:
    performers_field_str = format_performers_field(stash_context.scene.performers, settings)
    performers_field_str = apply_text_replacements(performers_field_str, settings.replacements)

    return performers_field_str


def format_performers_field(performers: list[Performer], settings: PerformerFieldSettings) -> str:
    performers = filter_performers(
        performers=performers,
        exclude_genders=settings.exclude_genders,
    )
    performers = sort_performers(performers=performers, sort_by=settings.sort_by)
    performers = limit_performers(
        performers=performers,
        limit=settings.limit,
        limit_exceeded_behavior=settings.limit_exceeded_behavior,
    )
    return concat_performer_names(performers=performers, separator=settings.separator)


def concat_performer_names(performers: list[Performer], separator: str) -> str:
    return separator.join([performer.name for performer in performers])


def filter_performers(
    performers: list[Performer],
    exclude_genders: Optional[list[GenderEnum]] = None,
) -> list[Performer]:
    if exclude_genders is None:
        return performers

    filtered = [performer for performer in performers if performer.gender not in exclude_genders]

    return filtered


def limit_performers(
    performers: list[Performer],
    limit: Optional[int],
    limit_exceeded_behavior: Optional[PerformerLimitExceededBehavior] = None,
) -> list[Performer]:
    if (
        limit is not None
        and len(performers) > limit
        and limit_exceeded_behavior == PerformerLimitExceededBehavior.DISCARD
    ):
        return []

    return performers[:limit]


def sort_performers(performers: list[Performer], sort_by: Optional[list[PerformerSortKey]] = None) -> list[Performer]:
    if sort_by is None:
        sort_by = [PerformerSortKey.ID]

    for key in reversed(sort_by):
        if key == PerformerSortKey.FAVORITE:
            # "favorite" performers should come first, so reverse the list (descending)
            # Since True = 1 and False = 0, an ascending order would have the "favorite" performer last
            performers = sorted(performers, key=operator.attrgetter("favorite"), reverse=True)
            continue

        if key == PerformerSortKey.RATING:
            # Higher rated performers should come first, so reverse the list (descending)
            performers = sorted(performers, key=operator.attrgetter("rating100"), reverse=True)
            continue

        performers = sorted(performers, key=operator.attrgetter(key))

    return performers
