from lily.fields.watched_field import WatchedFieldSettings, format_watched_field
from tests.testing_model_creators.create_scene import create_scene


class TestWatchedField:
    def test_formats_watched_field_correctly(self):
        scene = create_scene(o_counter=1)
        assert format_watched_field(scene, WatchedFieldSettings()) == "✅"

        scene = create_scene(o_counter=0)
        assert format_watched_field(scene, WatchedFieldSettings()) == ""

        scene = create_scene(o_counter=None)
        assert format_watched_field(scene, WatchedFieldSettings()) == ""
