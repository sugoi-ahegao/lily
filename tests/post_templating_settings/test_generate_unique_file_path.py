from pathlib import Path

import pytest
from tests.testing_model_creators.create_video_file import create_video_file
from tests.testing_utils.patch_file_exists import patch_file_exists

from lily.process_video_file import generate_unique_file_path


def random_file_path() -> Path:
    return create_video_file().path


def test_file_path_is_unchanged_if_it_is_already_unique():
    file_path = Path("/[VIDEOS]/My Scene Title.mp4")

    with patch_file_exists([False]):
        assert generate_unique_file_path(random_file_path(), file_path, "_${num}") == Path(
            "/[VIDEOS]/My Scene Title.mp4"
        )


def test_new_unique_path_is_generated_if_file_already_exists():
    file_path = Path("/[VIDEOS]/My Scene Title.mp4")

    with patch_file_exists([True, False]):
        assert generate_unique_file_path(random_file_path(), file_path, "_${num}") == Path(
            "/[VIDEOS]/My Scene Title_1.mp4"
        )


def test_suffixes_template_is_configurable():
    file_path = Path("/[VIDEOS]/My Scene Title.mp4")

    with patch_file_exists([True, True, False]):
        assert generate_unique_file_path(random_file_path(), file_path, "_${num}") == Path(
            "/[VIDEOS]/My Scene Title_2.mp4"
        )

    with patch_file_exists([True, True, False]):
        assert generate_unique_file_path(random_file_path(), file_path, " (${num})") == Path(
            "/[VIDEOS]/My Scene Title (2).mp4"
        )

    with patch_file_exists([True, True, False]):
        assert generate_unique_file_path(random_file_path(), file_path, " - ${num}") == Path(
            "/[VIDEOS]/My Scene Title - 2.mp4"
        )


def test_error_is_raised_if_max_attempts_is_exceeded():
    file_path = Path("/[VIDEOS]/My Scene Title.mp4")

    with patch_file_exists(True):
        with pytest.raises(RuntimeError):
            generate_unique_file_path(random_file_path(), file_path, "_${num}")


def test_error_is_raised_if_duplicate_suffix_template_is_invalid():
    file_path = Path("/[VIDEOS]/My Scene Title.mp4")

    with pytest.raises(ValueError):
        generate_unique_file_path(random_file_path(), file_path, "no num template variable")

    with pytest.raises(ValueError):
        generate_unique_file_path(random_file_path(), file_path, "${num} ${random}")
