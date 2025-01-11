from typing import Optional

from lily.fields.field_studio import StudioFieldSettings, format_studio_field
from lily.helpers.studio_hierarchy import create_studio_hierarchy
from lily.models.core import BaseModelWithExactAttributes
from lily.models.stash_graphql_models.studio import Studio
from lily.stash_context import StashContext


class StudioHierarchyAsPathFieldSettings(BaseModelWithExactAttributes):
    studio: StudioFieldSettings = StudioFieldSettings()


def studio_hierarchy_as_path_field(stash_context: StashContext, settings: StudioHierarchyAsPathFieldSettings) -> str:
    return format_studio_hierarchy_as_path_field(stash_context.scene.studio, stash_context.studios, settings)


def format_studio_hierarchy_as_path_field(
    studio: Optional[Studio], all_studios: list[Studio], settings: StudioHierarchyAsPathFieldSettings
) -> str:
    if studio is None:
        return ""

    studio_hierarchy = create_studio_hierarchy(studio, all_studios)
    formatted_studio_names = [format_studio_field(studio, settings.studio) for studio in studio_hierarchy]

    return "/".join(formatted_studio_names)
