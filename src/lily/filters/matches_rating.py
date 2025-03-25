from lily.fields.common import satisfies_all_constraints
from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class MatchesRatingFilterSettings(BaseModelWithExactAttributes):
    constraint: str


def matches_rating(stash_context: StashContext, settings: MatchesRatingFilterSettings):
    scene_rating = stash_context.scene.rating100

    if scene_rating is None:
        return False

    return satisfies_all_constraints(scene_rating, settings.constraint)
