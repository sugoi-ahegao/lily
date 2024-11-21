from typing import Optional

from lily.models.stash_graphql_models.video_file import VideoFile


def format_source_video_dir_field(video_file: Optional[VideoFile]) -> str:
    if video_file is None:
        return ""

    return video_file.path.parent.resolve().as_posix()
