from types import NoneType
from typing import Optional

from lily.models.stash_graphql_models.video_file import VideoFile
from lily.stash_context import StashContext

SourceVideoDirFieldSettings = NoneType


def source_video_dir_field(stash_context: StashContext, settings: SourceVideoDirFieldSettings) -> str:
    return format_source_video_dir_field(stash_context.video_file, settings)


def format_source_video_dir_field(video_file: Optional[VideoFile], settings: SourceVideoDirFieldSettings) -> str:
    if video_file is None:
        return ""

    return video_file.path.parent.resolve().as_posix()
