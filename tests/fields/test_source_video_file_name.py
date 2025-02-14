from pathlib import Path

from tests.testing_model_creators.create_video_file import create_video_file

from lily.fields.field_source_video_file_name import format_source_video_file_name_field


class TestSourceVideoFileNameField:
    def test_formats_source_video_file_name_correctly(self):
        video_file = create_video_file(file_path=Path("path/to/My Video File.mp4"))

        expected = "My Video File"
        actual = format_source_video_file_name_field(video_file, None)

        assert expected == actual
