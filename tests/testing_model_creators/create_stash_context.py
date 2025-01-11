from pathlib import Path
from typing import Optional

from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_video_file import create_video_file

from lily.models.stash_graphql_models.scene import Scene
from lily.models.stash_graphql_models.studio import Studio
from lily.models.stash_graphql_models.tag import Tag
from lily.models.stash_graphql_models.video_file import VideoFile
from lily.stash_context import StashContext


def create_stash_context(
    scene: Optional[Scene] = None,
    video_file: Optional[VideoFile] = None,
    studios: Optional[list[Studio]] = None,
    tags: Optional[list[Tag]] = None,
    stash_libraries: Optional[list[Path]] = None,
) -> StashContext:
    if scene is None:
        scene = create_scene()

    if video_file is None:
        video_file = create_video_file()

    if studios is None:
        studios = []

    if tags is None:
        tags = []

    if stash_libraries is None:
        stash_libraries = []

    return StashContext(scene=scene, video_file=video_file, studios=studios, tags=tags, stash_libraries=stash_libraries)
