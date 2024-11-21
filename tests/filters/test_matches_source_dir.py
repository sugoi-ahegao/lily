from pathlib import Path

from lily.filters.matches_source_dir import matches_source_dir
from tests.testing_model_creators.create_stash_context import create_stash_context
from tests.testing_model_creators.create_video_file import create_video_file


class TestMatchesSourceDirFilter:
    def test_matches_source_dir(self):
        video_file_path = Path("/[VIDEOS]/Scene Video.mp4")

        stash_ctx = create_stash_context(video_file=create_video_file(video_file_path))

        assert matches_source_dir(stash_ctx, Path("/[VIDEOS]"))
        assert matches_source_dir(stash_ctx, Path("/[VIDEOS]/"))
        assert matches_source_dir(stash_ctx, Path("/"))
        assert matches_source_dir(stash_ctx, Path("/[VIDEOS]/subfolder/.."))

        assert not matches_source_dir(stash_ctx, Path("/[VIDEOS]/subfolder"))
