from lily.stash_context import StashContext

MatchesHasStashIDFilterSettings = bool


def matches_has_stash_id(stash_context: StashContext, should_have_stash_id: MatchesHasStashIDFilterSettings) -> bool:
    if not should_have_stash_id:
        return len(stash_context.scene.stash_ids) == 0

    return len(stash_context.scene.stash_ids) > 0
