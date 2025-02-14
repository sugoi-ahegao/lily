from pathlib import Path

from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_stash_context import create_stash_context
from tests.testing_model_creators.create_video_file import create_video_file

from lily.fields.common import TextReplacementSetting
from lily.fields.field_title import Capitalization, TitleFieldSettings, format_title_field, title_field


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

    def test_remove_prefix(self):
        scene = create_scene(title="My Scene Title")

        expected = "Scene Title"
        actual = format_title_field(scene.title, TitleFieldSettings(remove_prefixes=["My"]))
        assert expected == actual

    def test_remove_multiple_prefixes(self):
        scene = create_scene(title="My Scene Title")

        expected = "Title"
        actual = format_title_field(scene.title, TitleFieldSettings(remove_prefixes=["My", "Scene"]))
        assert expected == actual

    def test_remove_prefix_with_no_match(self):
        scene = create_scene(title="My Scene Title")

        expected = "My Scene Title"
        actual = format_title_field(scene.title, TitleFieldSettings(remove_prefixes=["Not"]))
        assert expected == actual

    def test_remove_prefix_is_case_sensitive(self):
        scene = create_scene(title="My Scene Title")

        expected = "My Scene Title"
        actual = format_title_field(scene.title, TitleFieldSettings(remove_prefixes=["my"]))
        assert expected == actual


class TestTitleFieldFallback:
    def test_fallback_to_file_name_when_scene_title_is_none(self):
        scene = create_scene(title=None)
        video_file = create_video_file(file_path=Path("/path/to/video_file_name.mp4"))

        stash_context = create_stash_context(scene=scene, video_file=video_file)

        expected = ""
        actual = title_field(stash_context, TitleFieldSettings())
        assert expected == actual

        expected = "video_file_name"
        actual = title_field(stash_context, TitleFieldSettings(fallback_to_source_video_file_name=True))
        assert expected == actual

    def test_fallback_to_file_name_when_scene_title_is_empty(self):
        scene = create_scene(title="")
        video_file = create_video_file(file_path=Path("/path/to/video_file_name.mp4"))

        stash_context = create_stash_context(scene=scene, video_file=video_file)

        expected = ""
        actual = title_field(stash_context, TitleFieldSettings())
        assert expected == actual

        expected = "video_file_name"
        actual = title_field(stash_context, TitleFieldSettings(fallback_to_source_video_file_name=True))
        assert expected == actual

    def test_fallback_to_file_name_when_scene_title_is_whitespace(self):
        scene = create_scene(title="   ")
        video_file = create_video_file(file_path=Path("/path/to/video_file_name.mp4"))

        stash_context = create_stash_context(scene=scene, video_file=video_file)

        expected = ""
        actual = title_field(stash_context, TitleFieldSettings())
        assert expected == actual

        expected = "video_file_name"
        actual = title_field(stash_context, TitleFieldSettings(fallback_to_source_video_file_name=True))
        assert expected == actual

    def test_other_title_field_settings_are_not_applied(self):
        scene = create_scene(title=None)
        video_file = create_video_file(file_path=Path("/path/to/video_file_name.mp4"))

        stash_context = create_stash_context(scene=scene, video_file=video_file)

        expected = "video_file_name"
        actual = title_field(
            stash_context,
            TitleFieldSettings(
                capitalization=Capitalization.UPPERCASE,
                remove_prefixes=["video"],
                replacements=[TextReplacementSetting(find="file", replace="clip")],
                fallback_to_source_video_file_name=True,
            ),
        )
        assert expected == actual
