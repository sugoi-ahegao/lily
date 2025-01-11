from types import NoneType
from typing import Optional

from lily.models.stash_graphql_models.video_file import VideoFile
from lily.stash_context import StashContext

ResolutionFieldSettings = NoneType


def resolution_field(stash_context: StashContext, settings: ResolutionFieldSettings) -> str:
    return format_resolution_field(stash_context.video_file, settings)


def format_resolution_field(video_file: Optional[VideoFile], settings: ResolutionFieldSettings) -> str:
    if video_file is None:
        return ""

    if video_file.height > video_file.width:
        return "Vertical"

    if video_file.height >= 4320:
        return "8k"
    elif video_file.height >= 3384:
        return "6k"
    elif video_file.height >= 2880:
        return "5k"
    elif video_file.height >= 2160:
        return "4k"
    elif video_file.height >= 1440:
        return "2k"
    elif video_file.height >= 1080:
        return "1080p"
    else:
        return f"{video_file.height}p"
