from pathlib import Path
from typing import Optional

from lily.models.stash_graphql_models.video_file import VideoFile
from tests.testing_utils.generate_random_unique_id import generate_random_unique_id
from tests.testing_utils.generic import generic


def create_video_file(
    file_path: Optional[Path] = None, width: Optional[int] = None, height: Optional[int] = None
) -> VideoFile:
    if file_path is None:
        file_name = f"{generic.text.word()}.mp4"
        file_dir = generic.path.project_dir()
        file_path = Path(file_dir) / Path(file_name)

    else:
        file_name = str(file_path.name)
        file_dir = str(file_path.parent)
        file_path = file_path

    if width is None:
        width = 1920

    if height is None:
        height = 1080

    return VideoFile.model_validate(
        {
            "id": generate_random_unique_id(),
            "path": file_path,
            "basename": file_name,
            "parent_folder_id": file_dir,
            "mod_time": generic.datetime.datetime(),
            "size": generic.random.randint(1, 9_999_999_999),
            "width": width,
            "height": height,
            "duration": generic.random.random(),
            "video_codec": "h264",
            "audio_codec": "acc",
            "frame_rate": generic.random.random(),
            "bit_rate": generic.random.randint(1, 30_000_000),
            "created_at": generic.datetime.datetime(),
            "updated_at": generic.datetime.datetime(),
        }
    )
