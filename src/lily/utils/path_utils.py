from pathlib import Path


def dir_exists(path: Path):
    return path.is_dir()


def file_exists(path: Path):
    return path.is_file()


def are_paths_equal(path1: Path, path2: Path) -> bool:
    return path1.resolve() == path2.resolve()


def are_paths_on_same_drive(path_a: Path, path_b: Path) -> bool:
    return path_a.anchor == path_b.anchor
