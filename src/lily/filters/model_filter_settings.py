from typing import Any, Callable, Optional, Self

from pydantic import model_validator

from lily.filters.matches_any_source_dirs import MatchesAnySourceDirFilterSettings, matches_any_source_dir
from lily.filters.matches_any_studio import MatchesAnyStudioFilterSettings, matches_any_studio
from lily.filters.matches_any_tag import MatchesAnyTagFilterSettings, matches_any_tag
from lily.filters.matches_o_counter import MatchesOCounterFilterSettings, matches_o_counter
from lily.filters.matches_organized import MatchesOrganizedFilterSettings, matches_organized
from lily.filters.matches_source_dir import MatchesSourceDirFilterSettings, matches_source_dir
from lily.filters.matches_stash_id import MatchesStashIDFilterSettings, matches_stash_id
from lily.filters.matches_studio import MatchesStudioFilterSettings, matches_studio
from lily.filters.matches_tag import MatchesTagFilterSettings, matches_tag
from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class FilterSettings(BaseModelWithExactAttributes):
    matches_organized: Optional[MatchesOrganizedFilterSettings] = None
    matches_studio: Optional[MatchesStudioFilterSettings] = None
    matches_any_studio: Optional[MatchesAnyStudioFilterSettings] = None
    matches_source_dir: Optional[MatchesSourceDirFilterSettings] = None
    matches_any_source_dir: Optional[MatchesAnySourceDirFilterSettings] = None
    matches_stash_id: Optional[MatchesStashIDFilterSettings] = None
    matches_tag: Optional[MatchesTagFilterSettings] = None
    matches_any_tag: Optional[MatchesAnyTagFilterSettings] = None
    matches_o_counter: Optional[MatchesOCounterFilterSettings] = None

    @model_validator(mode="after")
    def check_model_contains_settings_for_entire_filter_registry(self) -> Self:
        for filter_registry_key in filter_registry.keys():
            try:
                getattr(self, filter_registry_key)
            except AttributeError as err:
                raise AssertionError(f"No setting found for filter: '{filter_registry_key}'") from err

        return self

    @model_validator(mode="after")
    def check_filter_registry_contains_entry_for_all_settings(self) -> Self:
        for field_name in self.model_fields:
            try:
                filter_registry[field_name]
            except KeyError as err:
                raise AssertionError(f"No entry in filter registry for filter setting: '{field_name}'") from err

        return self


filter_registry: dict[str, Callable[[StashContext, Any], bool]] = {
    "matches_organized": matches_organized,
    "matches_studio": matches_studio,
    "matches_any_studio": matches_any_studio,
    "matches_source_dir": matches_source_dir,
    "matches_any_source_dir": matches_any_source_dir,
    "matches_stash_id": matches_stash_id,
    "matches_tag": matches_tag,
    "matches_any_tag": matches_any_tag,
    "matches_o_counter": matches_o_counter,
}
