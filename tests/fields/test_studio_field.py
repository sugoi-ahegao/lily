import pytest
from tests.testing_model_creators.create_studio import create_studio

from lily.fields.field_studio import StudioFieldSettings, format_studio_field


class TestStudioField:
    def test_formats_studio_name_correctly(self):
        studio = create_studio()

        expected = studio.name
        actual = format_studio_field(studio, StudioFieldSettings())

        assert expected == actual

    def test_returns_empty_string_for_none_studio(self):
        expected = ""
        actual = format_studio_field(None, StudioFieldSettings())

        assert expected == actual

    def test_formats_studio_with_template(self):
        studio = create_studio(name="Studio Name")

        studio_template = "[${studio}]"

        expected = f"[{studio.name}]"
        actual = format_studio_field(studio, StudioFieldSettings(template=studio_template))

        assert expected == actual

        studio_template = " (${studio} abc)"

        expected = f" ({studio.name} abc)"
        actual = format_studio_field(studio, StudioFieldSettings(template=studio_template))

        assert expected == actual

    def test_raises_error_for_invalid_studio_template(self):
        studio = create_studio(name="Studio Name")

        with pytest.raises(ValueError):
            format_studio_field(studio, StudioFieldSettings(template=""))

        with pytest.raises(ValueError):
            format_studio_field(studio, StudioFieldSettings(template="${studio"))

        with pytest.raises(ValueError):
            format_studio_field(studio, StudioFieldSettings(template="${studio} ${another_field}"))

    def test_removes_spaces_when_squeezes_studio_name_is_true(self):
        studio = create_studio(name="Studio Name")

        expected = "StudioName"
        actual = format_studio_field(studio, StudioFieldSettings(squeeze_name=True))

        assert expected == actual
