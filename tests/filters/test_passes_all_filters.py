from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_stash_context import create_stash_context
from tests.testing_model_creators.create_studio import create_studio

from lily.filters.matches_organized import MatchesOrganizedFilterSettings
from lily.filters.matches_stash_id import MatchesStashIDFilterSettings
from lily.filters.matches_studio import MatchesStudioFilterSettings
from lily.filters.model_filter_settings import FilterSettings
from lily.filters.passes_all_filters import passes_all_filters


class TestPassesAllFilters:
    def test_scene_passes_organized_filter(self):
        scene = create_scene(organized=True)

        assert passes_all_filters(
            create_stash_context(scene=scene),
            FilterSettings(matches_organized=MatchesOrganizedFilterSettings(value=True)),
        )
        assert not passes_all_filters(
            create_stash_context(scene=scene),
            FilterSettings(matches_organized=MatchesOrganizedFilterSettings(value=False)),
        )

        scene = create_scene(organized=False)

        assert not passes_all_filters(
            create_stash_context(scene=scene),
            FilterSettings(matches_organized=MatchesOrganizedFilterSettings(value=True)),
        )
        assert passes_all_filters(
            create_stash_context(scene=scene),
            FilterSettings(matches_organized=MatchesOrganizedFilterSettings(value=False)),
        )

    def test_scene_passes_studio_filter_by_name(self):
        parent_studio = create_studio(name="My Studio")
        child_studio = create_studio(parent_studio=parent_studio, name="My Child Studio")
        studios = [parent_studio, child_studio]

        scene = create_scene(studio=child_studio)

        assert passes_all_filters(
            create_stash_context(scene=scene, studios=studios),
            FilterSettings(matches_studio=MatchesStudioFilterSettings(name=child_studio.name)),
        )

        assert not passes_all_filters(
            create_stash_context(scene=scene, studios=studios),
            FilterSettings(matches_studio=MatchesStudioFilterSettings(name="Non-Existing Studio")),
        )

    def test_scene_passes_studio_filter_with_include_sub_studios(self):
        grandparent_studio = create_studio(name="Grandparent Studio")
        parent_studio = create_studio(parent_studio=grandparent_studio, name="My Studio")
        child_studio = create_studio(parent_studio=parent_studio, name="My Child Studio")
        random_studio = create_studio(name="Random Studio")
        studios = [grandparent_studio, parent_studio, child_studio, random_studio]

        scene = create_scene(studio=child_studio)

        assert passes_all_filters(
            create_stash_context(scene=scene, studios=studios),
            FilterSettings(
                matches_studio=MatchesStudioFilterSettings(name=grandparent_studio.name, include_sub_studios=True)
            ),
        )

        assert passes_all_filters(
            create_stash_context(scene=scene, studios=studios),
            FilterSettings(
                matches_studio=MatchesStudioFilterSettings(name=parent_studio.name, include_sub_studios=True)
            ),
        )

        assert passes_all_filters(
            create_stash_context(scene=scene, studios=studios),
            FilterSettings(matches_studio=MatchesStudioFilterSettings(id=child_studio.id, include_sub_studios=True)),
        )

        assert not passes_all_filters(
            create_stash_context(scene=scene, studios=studios),
            FilterSettings(matches_studio=MatchesStudioFilterSettings(id=random_studio.id, include_sub_studios=True)),
        )

    def test_matches_has_stash_id_filter(self):
        stash_ids = [{"stash_id": "some-stash-id", "endpoint": "some-endpoint"}]

        ctx = create_stash_context(scene=create_scene(stash_ids=stash_ids))
        assert (
            passes_all_filters(ctx, FilterSettings(matches_stash_id=MatchesStashIDFilterSettings(value="not null")))
            is True
        )

        ctx = create_stash_context(scene=create_scene(stash_ids=[]))
        assert (
            passes_all_filters(ctx, FilterSettings(matches_stash_id=MatchesStashIDFilterSettings(value="not null")))
            is False
        )
