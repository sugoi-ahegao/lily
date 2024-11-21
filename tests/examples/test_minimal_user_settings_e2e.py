from pathlib import Path

from lily.models.user_settings.user_settings import load_user_settings
from lily.process_video_file import process_video_file
from lily.utils.load_yaml_file import load_yaml_file
from lily.utils.path_utils import are_paths_equal
from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_stash_context import create_stash_context
from tests.testing_model_creators.create_video_file import create_video_file


def load_minimal_user_settings():
    user_settings_path = Path("./examples/user_settings_minimal.yaml")
    user_settings_dict = load_yaml_file(user_settings_path)

    return load_user_settings(user_settings_dict)


def test_minimal_user_settings():
    scene = create_scene(title="My Scene Title")

    expected_file_path = Path("/[VIDEOS]/My Scene Title.mp4")

    actual_file_path = process_video_file(
        create_stash_context(scene=scene, video_file=create_video_file()), load_minimal_user_settings()
    )

    assert actual_file_path is not None
    assert are_paths_equal(expected_file_path, actual_file_path)
