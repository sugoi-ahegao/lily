import datetime
from typing import Optional

from lily.models.core import BaseModelWithExactAttributes
from lily.models.stash_graphql_models.performer import Performer
from lily.models.stash_graphql_models.studio import Studio
from lily.models.stash_graphql_models.tag import PartialTag
from lily.models.stash_graphql_models.video_file import VideoFile


class StashID(BaseModelWithExactAttributes):
    stash_id: str
    endpoint: str


class Scene(BaseModelWithExactAttributes):
    id: int
    title: Optional[str]
    details: Optional[str]
    date: Optional[datetime.date]
    rating100: Optional[int]
    organized: bool
    o_counter: Optional[int]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    stash_ids: list[StashID]
    files: list[VideoFile]
    studio: Optional[Studio]
    tags: list[PartialTag]
    performers: list[Performer]


SCENE_FRAGMENT = """
fragment SceneFragment on Scene {
    id
    title
    details
    date
    rating100
    organized
    o_counter
    created_at
    updated_at
    stash_ids {
        stash_id
        endpoint
    }
    files {
        ...VideoFileFragment
    }
    studio {
        ...StudioFragment
    }
    tags {
        ...PartialTagFragment
    }
    performers {
        ...PerformerFragment
    }
}
"""
