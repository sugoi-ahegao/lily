from typing import Optional

from lily.helpers.studio_hierarchy import create_studio_hierarchy
from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class MatchesStudioFilterSettings(BaseModelWithExactAttributes):
    name: Optional[str] = None
    id: Optional[int] = None
    include_sub_studios: bool = False


def matches_studio(stash_context: StashContext, matches_studio_filter: MatchesStudioFilterSettings) -> bool:
    if stash_context.scene.studio is None:
        return False

    scene_studio = stash_context.scene.studio

    if matches_studio_filter.name is not None:
        if matches_studio_filter.name == scene_studio.name:
            return True

    if matches_studio_filter.id is not None:
        if matches_studio_filter.id == scene_studio.id:
            return True

    if matches_studio_filter.include_sub_studios:
        hierarchy = create_studio_hierarchy(scene_studio, stash_context.studios)

        for studio in hierarchy:
            if matches_studio_filter.name is not None:
                if matches_studio_filter.name == studio.name:
                    return True

            if matches_studio_filter.id is not None:
                if matches_studio_filter.id == studio.id:
                    return True

    return False
