from tests.testing_model_creators.create_scene import create_scene

from lily.fields.field_title import Capitalization, TitleFieldSettings, format_title_field


class TestTitleField:
    def test_formats_title_correctly(self):
        scene = create_scene(title="My Scene Title")
        assert format_title_field(scene.title, TitleFieldSettings()) == "My Scene Title"

    def test_formats_title_correctly_with_capitalization(self):
        scene = create_scene(title="My Scene Title")

        expected = "MY SCENE TITLE"
        actual = format_title_field(scene.title, TitleFieldSettings(capitalization=Capitalization.UPPERCASE))
        assert expected == actual

        expected = "my scene title"
        actual = format_title_field(scene.title, TitleFieldSettings(capitalization=Capitalization.LOWERCASE))
        assert expected == actual

        expected = "My Scene Title"
        actual = format_title_field(scene.title, TitleFieldSettings(capitalization=Capitalization.TITLE))
