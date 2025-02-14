from lily.models.core import BaseModelWithExactAttributes, NonEmptyString


class PartialTag(BaseModelWithExactAttributes):
    id: int
    name: NonEmptyString

    @staticmethod
    def from_tag(tag: "Tag") -> "PartialTag":
        return PartialTag.model_validate(tag, from_attributes=True)

    @staticmethod
    def from_tags(tags: list["Tag"]) -> list["PartialTag"]:
        return [PartialTag.from_tag(tag) for tag in tags]


class Tag(BaseModelWithExactAttributes):
    id: int
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
