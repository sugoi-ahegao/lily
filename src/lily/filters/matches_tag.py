from collections import deque
from typing import Optional, Self

from pydantic import model_validator

from lily.helpers.tag_helpers import get_sub_tags, get_tag
from lily.models.core import BaseModelWithExactAttributes
from lily.models.stash_graphql_models.tag import PartialTag, Tag
from lily.stash_context import StashContext


class MatchesTagFilterSettings(BaseModelWithExactAttributes):
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


def matches_tag(stash_context: StashContext, settings: MatchesTagFilterSettings):
    scene_tag_ids = [scene_tag.id for scene_tag in stash_context.scene.tags]

    target_tag = get_tag(id=settings.id, name=settings.name, tags=stash_context.tags)

    if not settings.include_sub_tags:
        if target_tag.id in scene_tag_ids:
            return True
        return False

    sub_tags = get_sub_tags(target_tag, stash_context.tags)
    target_tags: list[Tag] = [target_tag, *sub_tags]

    for target_tag in target_tags:
        if target_tag.id in scene_tag_ids:
            return True

    return False


def find_tag_with_name(name: str, all_tags: list[Tag]):
    for tag in all_tags:
        if tag.name == name:
            return tag


def find_tag_with_id(id: int, all_tags: list[Tag]):
    for tag in all_tags:
        if tag.id == id:
            return tag


def get_all_sub_tags(tag: Tag, all_tags: list[Tag]):
    sub_tags: list[PartialTag] = []

    queue = deque([tag])

    while len(queue) != 0:
        curr_tag = queue.pop()

        sub_tags.extend(curr_tag.children)

        for partial_child_tag in curr_tag.children:
            child_tag = find_tag_with_id(partial_child_tag.id, all_tags)

            assert child_tag is not None, f"Tag not found. ID: '{partial_child_tag.id}'"

            queue.append(child_tag)

    return sub_tags
