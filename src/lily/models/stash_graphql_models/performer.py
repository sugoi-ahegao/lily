import datetime
from enum import Enum
from typing import Optional

from lily.models.core import BaseModelWithExactAttributes, NonEmptyString
from lily.models.stash_graphql_models.tag import PartialTag


class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    TRANSGENDER_MALE = "TRANSGENDER_MALE"
    TRANSGENDER_FEMALE = "TRANSGENDER_FEMALE"
    INTERSEX = "INTERSEX"
    NON_BINARY = "NON_BINARY"


class Performer(BaseModelWithExactAttributes):
    id: int
    name: NonEmptyString
    disambiguation: Optional[str]
    gender: Optional[GenderEnum]
    birthdate: Optional[datetime.date]
    ethnicity: Optional[str]
    alias_list: list[str]
    favorite: bool
    tags: list[PartialTag]
    rating100: Optional[int]
    created_at: datetime.datetime
    updated_at: datetime.datetime


PERFORMER_FRAGMENT = """
fragment PerformerFragment on Performer {
    id
    name
    disambiguation
    gender
    birthdate
    ethnicity
    alias_list
    favorite
    tags {
        ...PartialTagFragment
    }
    rating100
    created_at
    updated_at
}
"""
