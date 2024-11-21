from lily.models.core import BaseModelWithExactAttributes, NonEmptyString


class PartialTag(BaseModelWithExactAttributes):
    id: NonEmptyString
    name: NonEmptyString


class Tag(BaseModelWithExactAttributes):
    id: NonEmptyString
    name: NonEmptyString
    aliases: list[str]
    description: str
    parents: list[PartialTag]
    children: list[PartialTag]
    parent_count: int
    child_count: int


PARTIAL_TAG_FRAGMENT = """
fragment PartialTagFragment on Tag {
    id
    name
}
"""

TAG_FRAGMENT = """
fragment TagFragment on Tag {
    id
    name
    aliases
    description
    parents {
        ...PartialTagFragment
    }
    children {
        ...PartialTagFragment
    }
    parent_count
    child_count
}
"""
