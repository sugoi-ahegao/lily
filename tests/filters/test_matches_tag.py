import pytest
from tests.testing_model_creators.create_scene import create_scene
from tests.testing_model_creators.create_stash_context import create_stash_context
from tests.testing_model_creators.create_tag import create_tag

from lily.filters.matches_tag import MatchesTagFilterSettings, matches_tag
from lily.models.stash_graphql_models.tag import PartialTag


class TestMatchesTag:
    def test_matches_tag_with_name(self):
        tag = create_tag(name="Test Tag")
        tags = [tag]
        partial_tags = PartialTag.from_tags(tags)

        stash_context = create_stash_context(scene=create_scene(tags=partial_tags), tags=tags)
        filter_settings = MatchesTagFilterSettings(name="Test Tag")

        assert matches_tag(stash_context, filter_settings)

    def test_matches_tag_with_id(self):
        tag = create_tag(id=3)
        tags = [tag]
        partial_tags = PartialTag.from_tags(tags)

        stash_context = create_stash_context(scene=create_scene(tags=partial_tags), tags=tags)
        filter_settings = MatchesTagFilterSettings(id=3)

        assert matches_tag(stash_context, filter_settings)

    def test_matches_tag_with_no_tags(self):
        stash_context = create_stash_context()
        filter_settings = MatchesTagFilterSettings(name="Non-existing Tag")

        with pytest.raises(AssertionError):
            matches_tag(stash_context, filter_settings)

    def test_matches_tag_with_no_match(self):
        tag_a = create_tag()
        tag_b = create_tag()

        tags = [tag_a, tag_b]
        scene = create_scene(tags=PartialTag.from_tags([tag_a]))
        stash_context = create_stash_context(scene=scene, tags=tags)
        filter_settings = MatchesTagFilterSettings(name=tag_b.name)

        assert matches_tag(stash_context, filter_settings) is False

    def test_matches_tag_with_sub_tag(self):
        tag_a = create_tag()
        tag_b = create_tag(parents=[tag_a])

        tags = [tag_a, tag_b]

        scene = create_scene(tags=PartialTag.from_tags([tag_b]))
        stash_context = create_stash_context(scene=scene, tags=tags)
        filter_settings_with_tag_id = MatchesTagFilterSettings(id=tag_a.id, include_sub_tags=True)
        filter_settings_with_tag_name = MatchesTagFilterSettings(name=tag_a.name, include_sub_tags=True)

        assert matches_tag(stash_context, filter_settings_with_tag_id)
        assert matches_tag(stash_context, filter_settings_with_tag_name)

    def test_matches_tag_with_sub_tags_on_two_levels(self):
        tag_a = create_tag()
        tag_b = create_tag(parents=[tag_a])
        tag_c = create_tag(parents=[tag_b])

        tags = [tag_a, tag_b, tag_c]

        scene = create_scene(tags=PartialTag.from_tags([tag_c]))
        stash_context = create_stash_context(scene=scene, tags=tags)
        filter_settings_with_tag_id = MatchesTagFilterSettings(id=tag_a.id, include_sub_tags=True)
        filter_settings_with_tag_name = MatchesTagFilterSettings(name=tag_a.name, include_sub_tags=True)

        assert matches_tag(stash_context, filter_settings_with_tag_id)
        assert matches_tag(stash_context, filter_settings_with_tag_name)

    def test_matches_tag_with_sub_tags_with_no_match(self):
        tag_a = create_tag()
        tag_b = create_tag(parents=[tag_a])
        tag_c = create_tag(parents=[tag_b])
        tag_d = create_tag()

        tags = [tag_a, tag_b, tag_c, tag_d]

        scene = create_scene(tags=PartialTag.from_tags([tag_d]))
        stash_context = create_stash_context(scene=scene, tags=tags)
        filter_settings_with_tag_id = MatchesTagFilterSettings(id=tag_a.id, include_sub_tags=True)
        filter_settings_with_tag_name = MatchesTagFilterSettings(name=tag_a.name, include_sub_tags=True)

        assert matches_tag(stash_context, filter_settings_with_tag_id) is False
        assert matches_tag(stash_context, filter_settings_with_tag_name) is False

    def test_matches_tag_with_deeply_nested_sub_tags(self):
        first_tag = create_tag()
        tags = [first_tag]

        curr_tag = first_tag
        for _ in range(100):
            next_tag = create_tag(parents=[curr_tag])
            curr_tag = next_tag

            tags.append(curr_tag)

        last_tag = tags[-1]
        scene = create_scene(tags=PartialTag.from_tags([last_tag]))
        stash_context = create_stash_context(scene=scene, tags=tags)
        filter_settings_with_tag_id = MatchesTagFilterSettings(id=first_tag.id, include_sub_tags=True)
        filter_settings_with_tag_name = MatchesTagFilterSettings(name=first_tag.name, include_sub_tags=True)

        assert matches_tag(stash_context, filter_settings_with_tag_id)
        assert matches_tag(stash_context, filter_settings_with_tag_name)

    def test_invalid_filter_settings(self):
        with pytest.raises(ValueError):
            # Neither name or id set
            MatchesTagFilterSettings()

        with pytest.raises(ValueError):
            # Both name and id set
            MatchesTagFilterSettings(name="Test Tag", id=3)
