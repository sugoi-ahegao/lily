from lily.filters.matches_studio import MatchesStudioFilterSettings, matches_studio
from lily.stash_context import StashContext

MatchesAnyStudioFilterSettings = list[MatchesStudioFilterSettings]


def matches_any_studio(run_context: StashContext, matches_any_studio_filter: MatchesAnyStudioFilterSettings) -> bool:
    if run_context.scene.studio is None:
        return False

    return any(
        matches_studio(run_context, matches_studio_filter) for matches_studio_filter in matches_any_studio_filter
    )
