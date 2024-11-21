from typing import Optional

from lily.fields.studio_field import StudioFieldSettings, format_studio_field
from lily.helpers.studio_hierarchy import create_studio_hierarchy
from lily.models.core import BaseModelWithExactAttributes
from lily.models.stash_graphql_models.studio import Studio


class StudioHierarchyFieldSettings(BaseModelWithExactAttributes):
    separator: str = " "
    studio: StudioFieldSettings = StudioFieldSettings()


def format_studio_hierarchy_field(
    studio: Optional[Studio], all_studios: list[Studio], settings: StudioHierarchyFieldSettings
) -> str:
    if studio is None:
        return ""

    studio_hierarchy = create_studio_hierarchy(studio, all_studios)
    formatted_studio_names = [format_studio_field(studio, settings.studio) for studio in studio_hierarchy]
    return settings.separator.join(formatted_studio_names)
