from pathlib import Path


def remove_duplicate_dir_nesting(path: Path):
    path_parts = path.parts

    unique_path_parts: list[str] = []
    for index, path_part in enumerate(path_parts):
        if index == 0:
            unique_path_parts.append(path_part)
            continue

        if path_part == unique_path_parts[-1]:
            continue

        unique_path_parts.append(path_part)

    return Path(*unique_path_parts)
