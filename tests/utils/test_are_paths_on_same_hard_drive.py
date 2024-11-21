from pathlib import Path

from lily.utils.path_utils import are_paths_on_same_drive


def test_are_paths_on_same_drive_with_windows():
    path_1 = Path("C:\\Users\\adam\\Documents\\file.txt")
    path_2 = Path("C:\\System32\\file.txt")
    path_3 = Path("D:\\Users\\adam\\Documents\\file.txt")

    assert are_paths_on_same_drive(path_1, path_2)
    assert not are_paths_on_same_drive(path_1, path_3)
    assert not are_paths_on_same_drive(path_2, path_3)
