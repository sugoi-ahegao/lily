from pathlib import Path

from tests.testing_model_creators.create_video_file import create_video_file

from lily.fields.field_stash_library import StashLibraryFieldSettings, format_stash_library_field
from lily.utils.path_utils import are_paths_equal


class TestStashLibraryField:
    def test_formats_stash_library_correctly(self):
        video_file = create_video_file(file_path=Path("/stash-library/nested/folder/video.mp4"))

        stash_library_a = Path("/random/structure")
        stash_library_b = Path("/sources")
        stash_library_c = Path("/stash-library")

        stash_libraries = [stash_library_a, stash_library_b, stash_library_c]

        expected = stash_library_c
        actual = format_stash_library_field(
            video_file=video_file, stash_libraries=stash_libraries, settings=StashLibraryFieldSettings()
        )

        assert are_paths_equal(expected, Path(actual))
