from typing import Any, Callable, Self

from pydantic import model_validator

from lily.fields.field_date import DateFieldSettings, date_field
from lily.fields.field_performers import PerformerFieldSettings, performers_field
from lily.fields.field_rating import RatingFieldSettings, rating_field
from lily.fields.field_resolution import ResolutionFieldSettings, resolution_field
from lily.fields.field_source_video_dir import SourceVideoDirFieldSettings, source_video_dir_field
from lily.fields.field_source_video_file_name import SourceVideoFileNameFieldSettings, source_video_file_name_field
from lily.fields.field_stash_library import StashLibraryFieldSettings, stash_library_field
from lily.fields.field_studio import StudioFieldSettings, studio_field
from lily.fields.field_studio_hierarchy import StudioHierarchyFieldSettings, studio_hierarchy_field
from lily.fields.field_studio_hierarchy_as_path import (
    StudioHierarchyAsPathFieldSettings,
    studio_hierarchy_as_path_field,
)
from lily.fields.field_tags import TagsFieldSettings, tags_field
from lily.fields.field_title import TitleFieldSettings, title_field
from lily.fields.field_watched import WatchedFieldSettings, watched_field
from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class FieldSettings(BaseModelWithExactAttributes):
    date: DateFieldSettings = DateFieldSettings()
    performers: PerformerFieldSettings = PerformerFieldSettings()
    rating: RatingFieldSettings = RatingFieldSettings()
    resolution: ResolutionFieldSettings = ResolutionFieldSettings()
    source_video_dir: SourceVideoDirFieldSettings = SourceVideoDirFieldSettings()
    source_video_file_name: SourceVideoFileNameFieldSettings = SourceVideoFileNameFieldSettings()
    studio: StudioFieldSettings = StudioFieldSettings()
    studio_hierarchy_as_path: StudioHierarchyAsPathFieldSettings = StudioHierarchyAsPathFieldSettings()
    studio_hierarchy: StudioHierarchyFieldSettings = StudioHierarchyFieldSettings()
    title: TitleFieldSettings = TitleFieldSettings()
    watched: WatchedFieldSettings = WatchedFieldSettings()
    stash_library: StashLibraryFieldSettings = StashLibraryFieldSettings()
    tags: TagsFieldSettings = TagsFieldSettings()

    @model_validator(mode="after")
    def check_model_contains_settings_for_field_registry_file_dir(self) -> Self:
        for field_registry_key in field_registry_file_dir.keys():
            try:
                getattr(self, field_registry_key)
            except AttributeError:
                raise AssertionError(f"No setting found for file dir field: '{field_registry_key}'")

        return self

    @model_validator(mode="after")
    def check_model_contains_settings_for_field_registry_file_name(self) -> Self:
        for field_registry_key in field_registry_file_name.keys():
            try:
                getattr(self, field_registry_key)
            except AttributeError:
                raise AssertionError(f"No setting found for file name field: '{field_registry_key}'")

        return self


field_registry_file_dir: dict[str, Callable[[StashContext, Any], str]] = {
    "date": date_field,
    "rating": rating_field,
    "resolution": resolution_field,
    "source_video_dir": source_video_dir_field,
    "studio": studio_field,
    "studio_hierarchy_as_path": studio_hierarchy_as_path_field,
    "stash_library": stash_library_field,
}

field_registry_file_name: dict[str, Callable[[StashContext, Any], str]] = {
    "date": date_field,
    "performers": performers_field,
    "rating": rating_field,
    "resolution": resolution_field,
    "source_video_file_name": source_video_file_name_field,
    "studio": studio_field,
    "studio_hierarchy": studio_hierarchy_field,
    "title": title_field,
    "watched": watched_field,
    "tags": tags_field,
}
