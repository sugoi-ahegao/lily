import datetime
from typing import Optional

from lily.models.core import BaseModelWithExactAttributes, NonEmptyString
from lily.models.stash_graphql_models.tag import PartialTag


class PartialStudio(BaseModelWithExactAttributes):
    id: int
    name: NonEmptyString


class Studio(PartialStudio):
    parent_studio: Optional[PartialStudio]
    child_studios: list[PartialStudio]
    aliases: list[str]
    tags: list[PartialTag]
    rating100: Optional[int]
    favorite: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


PARTIAL_STUDIO_FRAGMENT = """
fragment PartialStudioFragment on Studio {
    id
    name
}
"""

STUDIO_FRAGMENT = """
fragment StudioFragment on Studio {
    id
    name
    parent_studio {
        ...PartialStudioFragment
    }
    child_studios {
        ...PartialStudioFragment
    }
    aliases
    tags {
        ...PartialTagFragment
    }
    rating100
    favorite
    created_at
    updated_at
}
"""
