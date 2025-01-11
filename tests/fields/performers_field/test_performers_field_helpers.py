from tests.testing_model_creators.create_performer import create_performer

from lily.fields.field_performers import (
    PerformerLimitExceededBehavior,
    concat_performer_names,
    filter_performers,
    limit_performers,
)
from lily.models.stash_graphql_models.performer import GenderEnum


class TestFilteringPerformers:
    def test_filtering_out_a_single_gender(self):
        performer1 = create_performer(gender=GenderEnum.MALE)
        performer2 = create_performer(gender=GenderEnum.FEMALE)

        performers = [performer1, performer2]

        expected = [performer2]
        actual = filter_performers(performers=performers, exclude_genders=[GenderEnum.MALE])

        assert expected == actual

    def test_filtering_out_multiple_genders(self):
        performer1 = create_performer(gender=GenderEnum.FEMALE)
        performer2 = create_performer(gender=GenderEnum.INTERSEX)
        performer3 = create_performer(gender=GenderEnum.MALE)

        performers = [performer1, performer2, performer3]

        expected = [performer1]
        actual = filter_performers(performers=performers, exclude_genders=[GenderEnum.MALE, GenderEnum.INTERSEX])

        assert expected == actual


class TestConcatenatingPerformers:
    def test_performer_separator_should_be_configurable(self):
        performer1 = create_performer()
        performer2 = create_performer()

        expected = f"{performer1.name}, {performer2.name}"
        actual = concat_performer_names(performers=[performer1, performer2], separator=", ")

        assert expected == actual

        expected = f"{performer1.name}; {performer2.name}"
        actual = concat_performer_names(performers=[performer1, performer2], separator="; ")

        assert expected == actual


class TestLimitingPerformers:
    def test_limit_is_applied(self):
        performer1 = create_performer()
        performer2 = create_performer()
        performer3 = create_performer()

        performers = [performer1, performer2, performer3]

        # limit amount of performers to 2
        expected = [performer1, performer2]
        actual = limit_performers(performers=performers, limit=2)

        assert expected == actual

        # if limit is greater than number of performers, return all performers
        expected = performers
        actual = limit_performers(performers=performers, limit=10)

        assert expected == actual

    def test_all_performers_are_returned_when_no_limit_is_applied(self):
        performer1 = create_performer()
        performer2 = create_performer()
        performer3 = create_performer()

        performers = [performer1, performer2, performer3]

        # if limit is None, return all performers
        expected = performers
        actual = limit_performers(performers=performers, limit=None)

        assert expected == actual

    def test_some_performers_are_returned_when_limit_is_exceeded_and_behavior_is_keep(self):
        performer1 = create_performer()
        performer2 = create_performer()
        performer3 = create_performer()

        performers = [performer1, performer2, performer3]

        # if behavior is keep and return performers until the limit
        expected = [performer1]
        actual = limit_performers(
            performers=performers, limit=1, limit_exceeded_behavior=PerformerLimitExceededBehavior.KEEP
        )

        assert expected == actual

    def test_no_performers_are_returned_when_limit_is_exceeded_and_behavior_is_discard(self):
        performer1 = create_performer()
        performer2 = create_performer()
        performer3 = create_performer()

        performers = [performer1, performer2, performer3]

        # if behavior is discard and number of performers exceeds limit, return no performers
        expected = []
        actual = limit_performers(
            performers=performers, limit=1, limit_exceeded_behavior=PerformerLimitExceededBehavior.DISCARD
        )

        assert expected == actual

        # if behavior is discard and number of performers is less than the limit, return all performers
        expected = performers
        actual = limit_performers(
            performers=performers, limit=10, limit_exceeded_behavior=PerformerLimitExceededBehavior.DISCARD
        )

        assert expected == actual
