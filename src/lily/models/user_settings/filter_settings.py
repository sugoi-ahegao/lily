from typing import Optional

from lily.filters.matches_any_source_dirs import MatchesAnySourceDirFilterSettings
from lily.filters.matches_any_studio import MatchesAnyStudioFilterSettings
from lily.filters.matches_has_stash_id import MatchesHasStashIDFilterSettings
from lily.filters.matches_organized_value import MatchesOrganizedValueFilterSettings
from lily.filters.matches_source_dir import MatchesSourceDirFilterSettings
from lily.filters.matches_studio import MatchesStudioFilterSettings
from lily.models.core import BaseModelWithExactAttributes


class FilterSettings(BaseModelWithExactAttributes):
    matches_organized_value: Optional[MatchesOrganizedValueFilterSettings] = None
    matches_studio: Optional[MatchesStudioFilterSettings] = None
    matches_any_studio: Optional[MatchesAnyStudioFilterSettings] = None
    matches_source_dir: Optional[MatchesSourceDirFilterSettings] = None
    matches_any_source_dir: Optional[MatchesAnySourceDirFilterSettings] = None
    matches_has_stash_id: Optional[MatchesHasStashIDFilterSettings] = None
