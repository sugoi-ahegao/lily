from pathlib import Path

from lily.filters.matches_source_dir import matches_source_dir
from lily.stash_context import StashContext

MatchesAnySourceDirFilterSettings = list[Path]


def matches_any_source_dir(stash_context: StashContext, source_dirs: MatchesAnySourceDirFilterSettings) -> bool:
    return any(matches_source_dir(stash_context, source_dir) for source_dir in source_dirs)
