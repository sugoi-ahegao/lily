from pathlib import Path

from lily.helpers.remove_duplicate_dir_nesting import remove_duplicate_dir_nesting
from lily.utils.path_utils import are_paths_equal


def test_remove_duplicate_dir_nesting_with_dir():
    duplicate_nested_path = Path("/my/folder/structure/structure")

    expected_path = Path("/my/folder/structure/")
    actual_path = remove_duplicate_dir_nesting(duplicate_nested_path)
    assert are_paths_equal(actual_path, expected_path)


def test_remove_duplicate_dir_nesting_with_file():
    duplicate_nested_path = Path("/Stash Libraries/80/80/file.mp4")

    expected_path = Path("/Stash Libraries/80/file.mp4")
    actual_path = remove_duplicate_dir_nesting(duplicate_nested_path)
    assert are_paths_equal(actual_path, expected_path)


def test_remove_duplicate_dir_nesting_with_file_and_dummy_nest():
    duplicate_nested_path = Path("/Stash Libraries/80/80/file/file.mp4")

    expected_path = Path("/Stash Libraries/80/file/file.mp4")
    actual_path = remove_duplicate_dir_nesting(duplicate_nested_path)
    assert are_paths_equal(actual_path, expected_path)
