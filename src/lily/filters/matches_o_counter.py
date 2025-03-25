from lily.fields.common import satisfies_all_constraints
from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class MatchesOCounterFilterSettings(BaseModelWithExactAttributes):
    constraint: str


def matches_o_counter(stash_context: StashContext, settings: MatchesOCounterFilterSettings):
    scene_o_counter = stash_context.scene.o_counter

    if scene_o_counter is None:
        return False

    return satisfies_all_constraints(scene_o_counter, settings.constraint)
