from tests.testing_model_creators.create_tag import create_tag

from lily.fields.field_tags import TagCriteria, TagsFieldSettings, format_tags_field
from lily.models.stash_graphql_models.tag import PartialTag


class TestTagsField:
    def test_tags_field_formats_correctly(self):
        tag1 = create_tag(id=1)
        tag2 = create_tag(id=2)
        tag3 = create_tag(id=3)

        tags = [tag1, tag2, tag3]
        partial_tags = PartialTag.from_tags(tags)

        expected = f"{tag1.name} {tag2.name} {tag3.name}"
        actual = format_tags_field(scene_tags=partial_tags, all_tags=tags, settings=TagsFieldSettings())

        assert expected == actual

    def test_tags_field_with_custom_separator(self):
        tag1 = create_tag(id=1)
        tag2 = create_tag(id=2)
        tag3 = create_tag(id=3)

        tags = [tag1, tag2, tag3]
        partial_tags = PartialTag.from_tags(tags)

        expected = f"{tag1.name},{tag2.name},{tag3.name}"
        actual = format_tags_field(scene_tags=partial_tags, all_tags=tags, settings=TagsFieldSettings(separator=","))

        assert expected == actual

    def test_tags_field_with_whitelist(self):
        tag1 = create_tag(id=1)
        tag2 = create_tag(id=2)
        tag3 = create_tag(id=3)

        tags = [tag1, tag2, tag3]
        partial_tags = PartialTag.from_tags(tags)

        expected = f"{tag2.name}"
        actual = format_tags_field(
            scene_tags=partial_tags, all_tags=tags, settings=TagsFieldSettings(whitelist=[TagCriteria(id=2)])
        )

        assert expected == actual

    def test_tags_field_with_blacklist(self):
        tag1 = create_tag(id=1)
        tag2 = create_tag(id=2)
        tag3 = create_tag(id=3)

        tags = [tag1, tag2, tag3]
        partial_tags = PartialTag.from_tags(tags)

        expected = f"{tag1.name} {tag3.name}"
        actual = format_tags_field(
            scene_tags=partial_tags, all_tags=tags, settings=TagsFieldSettings(blacklist=[TagCriteria(id=2)])
        )

        assert expected == actual

    def test_tags_field_with_whitelist_with_sub_tags(self):
        tag1 = create_tag(id=1)
        tag2 = create_tag(id=2, parents=[tag1])
        tag3 = create_tag(id=3, parents=[tag2])

        tags = [tag1, tag2, tag3]

        expected = f"{tag2.name} {tag3.name}"

        actual = format_tags_field(
            scene_tags=PartialTag.from_tags([tag2, tag3]),
            all_tags=tags,
            settings=TagsFieldSettings(whitelist=[TagCriteria(id=1, include_sub_tags=True)]),
        )

        assert expected == actual

    def test_tags_field_with_blacklist_with_sub_tags(self):
        tag1 = create_tag(id=1)
        tag2 = create_tag(id=2, parents=[tag1])
        tag3 = create_tag(id=3, parents=[tag2])

        tags = [tag1, tag2, tag3]

        expected = ""

        actual = format_tags_field(
            scene_tags=PartialTag.from_tags([tag2, tag3]),
            all_tags=tags,
            settings=TagsFieldSettings(blacklist=[TagCriteria(id=1, include_sub_tags=True)]),
        )

        assert expected == actual

    def test_tags_field_with_limit(self):
        tag1 = create_tag(id=1)
        tag2 = create_tag(id=2)
        tag3 = create_tag(id=3)

        tags = [tag1, tag2, tag3]
        partial_tags = PartialTag.from_tags(tags)

        expected = f"{tag1.name} {tag2.name}"
        actual = format_tags_field(scene_tags=partial_tags, all_tags=tags, settings=TagsFieldSettings(limit=2))

        assert expected == actual
