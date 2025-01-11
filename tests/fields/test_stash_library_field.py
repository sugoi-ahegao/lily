from pathlib import Path

from tests.testing_model_creators.create_video_file import create_video_file

from lily.fields.field_stash_library import StashLibraryFieldSettings, format_stash_library_field
from lily.utils.path_utils import are_paths_equal


def test_stash_library_field():
    video_file = create_video_file(file_path=Path("/stash-library/nested/folder/video.mp4"))

    stash_libraries = [Path("/random/structure"), Path("/sources"), Path("/stash-library")]

    expected = stash_libraries[2]
    actual = format_stash_library_field(
        video_file=video_file, stash_libraries=stash_libraries, settings=StashLibraryFieldSettings()
    )

    assert are_paths_equal(expected, Path(actual))
