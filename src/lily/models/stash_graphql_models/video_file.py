import datetime
from pathlib import Path

from lily.models.core import BaseModelWithExactAttributes, NonEmptyString


class VideoFile(BaseModelWithExactAttributes):
    id: int
    path: Path
    basename: NonEmptyString
    parent_folder_id: NonEmptyString
    mod_time: datetime.datetime
    size: int
    width: int
    height: int
    duration: float
    video_codec: NonEmptyString
    audio_codec: NonEmptyString
    frame_rate: float
    bit_rate: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


VIDEO_FILE_FRAGMENT = """
fragment VideoFileFragment on VideoFile {
    id
    path
    basename
    parent_folder_id
    mod_time
    size
    width
    height
    duration
    video_codec
    audio_codec
    frame_rate
    bit_rate
    created_at
    updated_at
}
"""
