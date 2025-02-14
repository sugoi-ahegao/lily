import operator
from enum import Enum
from typing import Optional, Self

from pydantic import model_validator

from lily.fields.common import TextReplacementSetting, apply_text_replacements
from lily.helpers.tag_helpers import get_sub_tags, get_tag
from lily.models.core import BaseModelWithExactAttributes
from lily.models.stash_graphql_models.tag import PartialTag, Tag
from lily.stash_context import StashContext


class TagsSortKey(str, Enum):
    ID = "id"
    NAME = "name"


class TagCriteria(BaseModelWithExactAttributes):
    name: Optional[str] = None
    id: Optional[int] = None
    include_sub_tags: bool = False

    @model_validator(mode="after")
    def require_name_xor_id(self) -> Self:
        if (self.name is None) and (self.id is None):
            raise ValueError("Either name or id is required")

        if (self.name is not None) and (self.id is not None):
            raise ValueError("Both name and id cannot be set")

        return self


class TagsFieldSettings(BaseModelWithExactAttributes):
    separator: str = " "
    sort_by: list[TagsSortKey] = [TagsSortKey.ID]
    limit: Optional[int] = None
    whitelist: Optional[list[TagCriteria]] = None
    blacklist: Optional[list[TagCriteria]] = None
    replacements: Optional[list[TextReplacementSetting]] = None

    @model_validator(mode="after")
    def mutually_exclusive_whitelist_and_blacklist(self) -> Self:
        if (self.whitelist is not None) and (self.blacklist is not None):
            raise ValueError("Both whitelist and blacklist cannot be set")

        return self


def tags_field(stash_context: StashContext, settings: TagsFieldSettings):
    tags_field_str = format_tags_field(stash_context.scene.tags, stash_context.tags, settings)
    tags_field_str = apply_text_replacements(tags_field_str, settings.replacements)

    return tags_field_str


def format_tags_field(scene_tags: list[PartialTag], all_tags: list[Tag], settings: TagsFieldSettings):
    scene_tags = sort_tags(scene_tags, sort_by=settings.sort_by)

    if settings.whitelist is not None:
        whitelist_tags = get_tags_with_criteria(settings.whitelist, all_tags)
        whitelist_tag_ids = [tag.id for tag in whitelist_tags]

        scene_tags = [scene_tag for scene_tag in scene_tags if scene_tag.id in whitelist_tag_ids]

    if settings.blacklist is not None:
        blacklist_tags = get_tags_with_criteria(settings.blacklist, all_tags)
        blacklist_tag_ids = [tag.id for tag in blacklist_tags]

        scene_tags = [scene_tag for scene_tag in scene_tags if scene_tag.id not in blacklist_tag_ids]

    scene_tags = limit_tags(scene_tags, settings.limit)

    return concat_tag_names(scene_tags, settings.separator)


def sort_tags(tags: list[PartialTag], sort_by: list[TagsSortKey]) -> list[PartialTag]:
    for key in reversed(sort_by):
        tags = sorted(tags, key=operator.attrgetter(key))

    return tags


def get_tags_with_criteria(tag_criteria_list: list[TagCriteria], tags: list[Tag]):
    matching_tags: list[Tag] = []

    for tag_criteria in tag_criteria_list:
        tag = get_tag(id=tag_criteria.id, name=tag_criteria.name, tags=tags)

        matching_tags.append(tag)

        if tag_criteria.include_sub_tags:
            sub_tags = get_sub_tags(tag, tags)
            matching_tags.extend(sub_tags)

    return matching_tags


def concat_tag_names(tags: list[PartialTag], separator: str) -> str:
    return separator.join([tag.name for tag in tags])


def limit_tags(tags: list[PartialTag], limit: Optional[int]):
    if limit is None:
        return tags

    if len(tags) <= limit:
        return tags

    return tags[:limit]
