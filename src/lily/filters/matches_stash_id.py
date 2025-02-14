from typing import Optional

from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class MatchesStashIDFilterSettings(BaseModelWithExactAttributes):
    value: Optional[str]


def matches_stash_id(stash_context: StashContext, settings: MatchesStashIDFilterSettings) -> bool:
    if settings.value is None:
        return len(stash_context.scene.stash_ids) == 0

    if settings.value.lower() == "not null":
        return len(stash_context.scene.stash_ids) > 0

    # Extract stash id strings from the stash id models to compare values
    stash_ids = [stash_id.stash_id for stash_id in stash_context.scene.stash_ids]

    return settings.value in stash_ids
