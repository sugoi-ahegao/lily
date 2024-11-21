from lily.fields.date_field import DateFieldSettings, format_date_field
from tests.testing_model_creators.create_scene import create_scene


class TestDateField:
    def test_formats_date_correctly(self):
        scene = create_scene(date="2021-12-31")
        assert format_date_field(scene.date, DateFieldSettings()) == "2021-12-31"

    def test_returns_empty_string_if_no_date(self):
        scene = create_scene(date=None)
        assert format_date_field(scene.date, DateFieldSettings()) == ""

    def test_formats_date_with_different_formats(self):
        scene = create_scene(date="2021-12-31")
        assert format_date_field(scene.date, DateFieldSettings(format="%m/%d/%Y")) == "12/31/2021"

        scene = create_scene(date="2021-12-31")
        assert format_date_field(scene.date, DateFieldSettings(format="%Y-%m-%d")) == "2021-12-31"

        scene = create_scene(date="2021-12-31")
        assert format_date_field(scene.date, DateFieldSettings(format="%B %d, %Y")) == "December 31, 2021"
