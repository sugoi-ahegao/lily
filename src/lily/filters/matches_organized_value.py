from lily.stash_context import StashContext

MatchesOrganizedValueFilterSettings = bool


def matches_organized_value(stash_context: StashContext, organized_value: MatchesOrganizedValueFilterSettings) -> bool:
    return stash_context.scene.organized == organized_value
