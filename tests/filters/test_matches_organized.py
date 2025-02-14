from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_stash_context import create_stash_context

from lily.filters.matches_organized import MatchesOrganizedFilterSettings, matches_organized


class TestMatchesOrganized:
    def test_organized_scene(self):
        scene = create_scene(organized=True)

        stash_ctx = create_stash_context(scene=scene)

        assert matches_organized(stash_ctx, MatchesOrganizedFilterSettings(value=True)) is True
        assert matches_organized(stash_ctx, MatchesOrganizedFilterSettings(value=False)) is False

    def test_unorganized_scene(self):
        scene = create_scene(organized=False)

        stash_ctx = create_stash_context(scene=scene)

        assert matches_organized(stash_ctx, MatchesOrganizedFilterSettings(value=True)) is False
        assert matches_organized(stash_ctx, MatchesOrganizedFilterSettings(value=False)) is True
