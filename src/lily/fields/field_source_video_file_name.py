from types import NoneType
from typing import Optional

from lily.models.stash_graphql_models.video_file import VideoFile
from lily.stash_context import StashContext

SourceVideoFileNameFieldSettings = NoneType


def source_video_file_name_field(stash_context: StashContext, settings: SourceVideoFileNameFieldSettings) -> str:
    return format_source_video_file_name_field(stash_context.video_file, settings)


def format_source_video_file_name_field(
    video_file: Optional[VideoFile], settings: SourceVideoFileNameFieldSettings
) -> str:
    if video_file is None:
        return ""

    return video_file.path.stem
