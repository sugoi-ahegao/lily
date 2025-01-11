import pytest
from tests.testing_model_creators.create_video_file import create_video_file

from lily.fields.field_resolution import ResolutionFieldSettings, format_resolution_field


class TestResolutionField:
    @pytest.mark.parametrize(
        "width, height, expected_name",
        [
            (7680, 4320, "8k"),
            (3840, 2160, "4k"),
            (2560, 1440, "2k"),
            (1920, 1080, "1080p"),
            (1280, 720, "720p"),
            (854, 480, "480p"),
            (640, 360, "360p"),
            (426, 240, "240p"),
        ],
    )
    def test_formats_common_resolutions(self, width: int, height: int, expected_name: str):
        video_file = create_video_file(width=width, height=height)
        assert format_resolution_field(video_file, ResolutionFieldSettings()) == expected_name

    def test_returns_empty_string_for_none_video_file(self):
        assert format_resolution_field(None, ResolutionFieldSettings()) == ""

    def test_recognizes_vertical_resolutions(self):
        video_file = create_video_file(width=1080, height=1920)
        assert format_resolution_field(video_file, ResolutionFieldSettings()) == "Vertical"

        video_file = create_video_file(width=1080, height=1350)
        assert format_resolution_field(video_file, ResolutionFieldSettings()) == "Vertical"
