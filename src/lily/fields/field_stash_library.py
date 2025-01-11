from pathlib import Path
from types import NoneType
from typing import Optional

from lily.models.stash_graphql_models.video_file import VideoFile
from lily.stash_context import StashContext

StashLibraryFieldSettings = NoneType


def stash_library_field(stash_context: StashContext, settings: StashLibraryFieldSettings) -> str:
    return format_stash_library_field(stash_context.video_file, stash_context.stash_libraries, settings)


def format_stash_library_field(
    video_file: Optional[VideoFile], stash_libraries: list[Path], settings: StashLibraryFieldSettings
) -> str:
    if video_file is None:
        return ""

    for stash_library in stash_libraries:
        if video_file.path.resolve().is_relative_to(stash_library.resolve()):
            return stash_library.resolve().as_posix()

    return ""
