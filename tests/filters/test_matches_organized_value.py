from lily.filters.matches_organized_value import matches_organized_value
from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_stash_context import create_stash_context


def test_organized_scene():
    scene = create_scene(organized=True)

    stash_ctx = create_stash_context(scene=scene)

    assert matches_organized_value(stash_ctx, True) is True
    assert matches_organized_value(stash_ctx, False) is False


def test_unorganized_scene():
    scene = create_scene(organized=False)

    stash_ctx = create_stash_context(scene=scene)

    assert matches_organized_value(stash_ctx, True) is False
    assert matches_organized_value(stash_ctx, False) is True
