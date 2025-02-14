from lily.filters.matches_tag import MatchesTagFilterSettings, matches_tag
from lily.stash_context import StashContext

MatchesAnyTagFilterSettings = list[MatchesTagFilterSettings]


def matches_any_tag(stash_context: StashContext, matches_any_tag_filter_settings: MatchesAnyTagFilterSettings) -> bool:
    if len(stash_context.scene.tags) == 0:
        return False

    return any(
        matches_tag(stash_context, matches_tag_filter_settings)
        for matches_tag_filter_settings in matches_any_tag_filter_settings
    )
