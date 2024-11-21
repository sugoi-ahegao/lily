from pathlib import Path
from unittest.mock import patch

import pytest
from lily.process_video_file import process_video_file
from lily.utils.path_utils import are_paths_equal
from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_stash_context import create_stash_context
from tests.testing_model_creators.create_user_settings import create_user_settings
from tests.testing_model_creators.create_video_file import create_video_file
from tests.testing_utils.patch_file_exists import patch_file_exists


def test_unique_path_is_generated_e2e():
    scene = create_scene(title="My Scene Title")
    stash_context = create_stash_context(scene=scene, video_file=create_video_file())

    template_file_dir = "/[VIDEOS]"
    template_file_name = "${title}"

    user_settings = create_user_settings(
        template_file_dir=template_file_dir,
        template_file_name=template_file_name,
        duplicate_suffix_template=" (${num})",
    )

    expected_file_path = Path("/[VIDEOS]/My Scene Title (1).mp4")
    with patch_file_exists([True, False]):
        actual_file_path = process_video_file(stash_context, user_settings)
        assert actual_file_path is not None
        assert are_paths_equal(expected_file_path, actual_file_path)

    expected_file_path = Path("/[VIDEOS]/My Scene Title (2).mp4")
    with patch_file_exists([True, True, False]):
        actual_file_path = process_video_file(stash_context, user_settings)
        assert actual_file_path is not None
        assert are_paths_equal(expected_file_path, actual_file_path)

    expected_file_path = Path("/[VIDEOS]/My Scene Title (3).mp4")
    with patch_file_exists([True, True, True, False]):
        actual_file_path = process_video_file(stash_context, user_settings)
        assert actual_file_path is not None
        assert are_paths_equal(expected_file_path, actual_file_path)

    with pytest.raises(RuntimeError):
        with patch_file_exists(True):
            actual_file_path = process_video_file(stash_context, user_settings)
            assert actual_file_path is not None
            assert are_paths_equal(expected_file_path, actual_file_path)


def test_file_path_is_not_renamed_if_new_file_path_is_same_as_existing_file_path():
    expected_file_path = Path("/[VIDEOS]/Scene Video.mp4")

    stash_context = create_stash_context(
        scene=create_scene(), video_file=create_video_file(file_path=expected_file_path)
    )
    user_settings = create_user_settings()

    with patch("lily.process_video_file.generate_file_dir") as mock_generate_file_dir:
        with patch("lily.process_video_file.generate_file_name") as mock_generate_file_name:
            mock_generate_file_dir.return_value = expected_file_path.parent
            mock_generate_file_name.return_value = expected_file_path.stem

            actual_file_path = process_video_file(stash_context, user_settings)

            assert actual_file_path is None
