from lily.filters.matches_studio import MatchesStudioFilterSettings, matches_studio
from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_stash_context import create_stash_context
from tests.testing_model_creators.create_studio import create_studio


def test_matches_studio_with_name():
    studio = create_studio(name="My Studio")

    stash_context = create_stash_context(scene=create_scene(studio=studio), studios=[studio])

    filter_settings = MatchesStudioFilterSettings(name="My Studio")
    assert matches_studio(stash_context, filter_settings)


def test_matches_studio_with_no_match():
    studio = create_studio()

    stash_context = create_stash_context(scene=create_scene(studio=studio), studios=[studio])

    filter_settings = MatchesStudioFilterSettings(name="Non-existing studio")

    assert matches_studio(stash_context, filter_settings) is False


def test_scene_with_no_studio():
    scene = create_scene(studio=None)

    stash_context = create_stash_context(scene=scene, studios=[create_studio()])

    filter_settings = MatchesStudioFilterSettings(name="My Studio")

    assert matches_studio(stash_context, filter_settings) is False


def test_with_no_studios():
    scene = create_scene(studio=None)

    stash_context = create_stash_context(scene=scene, studios=[])

    filter_settings = MatchesStudioFilterSettings(name="My Studio")

    assert matches_studio(stash_context, filter_settings) is False
