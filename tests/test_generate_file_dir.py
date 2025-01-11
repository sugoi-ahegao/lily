import pytest

from lily.fields.generate_file_path import generate_file_dir
from lily.fields.model_field_settings import FieldSettings
from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_stash_context import create_stash_context
from tests.testing_model_creators.create_studio import create_studio


def test_generate_file_dir_with_studio():
    scene = create_scene(studio=create_studio())

    assert scene.studio is not None, "Scene studio is not set"

    template = "${studio}"
    expected = f"{scene.studio.name}"
    actual = generate_file_dir(template, create_stash_context(scene=scene), FieldSettings())

    assert expected == actual


def test_generate_file_dir_with_unknown_field():
    template = "${unknown_field}"

    with pytest.raises(ValueError):
        generate_file_dir(template, create_stash_context(), FieldSettings())
