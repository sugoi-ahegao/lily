from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class MatchesOrganizedFilterSettings(BaseModelWithExactAttributes):
    value: bool


def matches_organized(stash_context: StashContext, settings: MatchesOrganizedFilterSettings) -> bool:
    return stash_context.scene.organized == settings.value
