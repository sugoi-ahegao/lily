from typing import Any, Callable, Optional

from lily.filters.matches_any_source_dirs import MatchesAnySourceDirFilterSettings, matches_any_source_dir
from lily.filters.matches_any_studio import MatchesAnyStudioFilterSettings, matches_any_studio
from lily.filters.matches_has_stash_id import MatchesHasStashIDFilterSettings, matches_has_stash_id
from lily.filters.matches_organized_value import MatchesOrganizedValueFilterSettings, matches_organized_value
from lily.filters.matches_source_dir import MatchesSourceDirFilterSettings, matches_source_dir
from lily.filters.matches_studio import MatchesStudioFilterSettings, matches_studio
from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class FilterSettings(BaseModelWithExactAttributes):
    matches_organized_value: Optional[MatchesOrganizedValueFilterSettings] = None
    matches_studio: Optional[MatchesStudioFilterSettings] = None
    matches_any_studio: Optional[MatchesAnyStudioFilterSettings] = None
    matches_source_dir: Optional[MatchesSourceDirFilterSettings] = None
    matches_any_source_dir: Optional[MatchesAnySourceDirFilterSettings] = None
    matches_has_stash_id: Optional[MatchesHasStashIDFilterSettings] = None


filter_registry: dict[str, Callable[[StashContext, Any], bool]] = {
    "matches_organized_value": matches_organized_value,
    "matches_studio": matches_studio,
    "matches_any_studio": matches_any_studio,
    "matches_source_dir": matches_source_dir,
    "matches_any_source_dir": matches_any_source_dir,
    "matches_has_stash_id": matches_has_stash_id,
}
