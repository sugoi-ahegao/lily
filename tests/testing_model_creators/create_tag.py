from typing import Optional

from tests.testing_utils.generate_random_unique_id import generate_random_unique_id
from tests.testing_utils.generic import generic

from lily.models.stash_graphql_models.tag import PartialTag, Tag


def create_tag(id: Optional[int] = None, name: Optional[str] = None, parents: Optional[list[Tag]] = None) -> Tag:
    if id is None:
        id = generate_random_unique_id()

    if name is None:
        name = generic.text.word()

    tag = Tag.model_validate(
        {
            "id": id,
            "name": name,
            "aliases": [],
            "description": "",
            "parents": [],
            "children": [],
            "parent_count": 0,
            "child_count": 0,
        }
    )

    if parents is not None:
        tag.parents = PartialTag.from_tags(parents)
        tag.parent_count = len(tag.parents)

        for parent in parents:
            parent.children.append(PartialTag.from_tag(tag))
            parent.child_count += 1

    return tag
