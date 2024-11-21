from lily.fields.performers_field import format_performers_field
from lily.file_path_template import generate_file_name
from lily.models.user_settings.field_settings import FieldSettings

from tests.testing_model_creators.create_performer import create_performer
from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_stash_context import create_stash_context


def test_generate_file_name_with_title():
    scene_title = "my scene title"

    scene = create_scene(title=scene_title)

    template = "${title}"
    expected = f"{scene_title}"
    actual = generate_file_name(template, create_stash_context(scene=scene), FieldSettings())

    assert expected == actual


def test_generate_file_name_with_title_and_date():
    scene_title = "test title"
    scene_date = "2024-01-01"

    scene = create_scene(title=scene_title, date=scene_date)

    template = "${title} ${date}"
    expected = f"{scene_title} {scene_date}"
    actual = generate_file_name(template, create_stash_context(scene=scene), FieldSettings())

    assert expected == actual


def test_generate_file_name_with_run_context():
    performers = [create_performer(), create_performer()]
    scene = create_scene(title="scene title", performers=performers)

    field_settings = FieldSettings()

    template = "${title} ${performers}"
    expected = f"{scene.title} {format_performers_field(performers, field_settings.performers)}"
    actual = generate_file_name(template, create_stash_context(scene=scene), field_settings)

    assert expected == actual
