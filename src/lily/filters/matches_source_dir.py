from pathlib import Path

from lily.stash_context import StashContext

MatchesSourceDirFilterSettings = Path


def matches_source_dir(stash_context: StashContext, source_dir: MatchesSourceDirFilterSettings) -> bool:
    return is_subdir(source_dir, stash_context.video_file.path)


def is_subdir(parent_dir: Path, child_dir: Path) -> bool:
    return child_dir.resolve().is_relative_to(parent_dir.resolve())
