from lily.stash_context import StashContext

MatchesOrganizedValueFilterSettings = bool


def matches_organized_value(run_context: StashContext, organized_value: MatchesOrganizedValueFilterSettings) -> bool:
    return run_context.scene.organized == organized_value
