from pathlib import Path

from tests.testing_model_creators.create_video_file import create_video_file

from lily.fields.field_source_video_dir import format_source_video_dir_field


class TestSourceVideoDirField:
    def test_formats_source_video_dir_correctly(self):
        video_file = create_video_file(file_path=Path("path/to/file.mp4"))

        expected = video_file.path.parent.resolve().as_posix()
        actual = format_source_video_dir_field(video_file, None)
        assert expected == actual
