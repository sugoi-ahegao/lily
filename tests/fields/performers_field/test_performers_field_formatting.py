from tests.testing_model_creators.create_performer import create_performer

from lily.fields.field_performers import (
    PerformerFieldSettings,
    format_performers_field,
)
from lily.models.stash_graphql_models.performer import GenderEnum


class TestPerformersFormatting:
    def test_performer_field_formatting(self):
        performer1 = create_performer(name="Mandy Muse", gender=GenderEnum.FEMALE, favorite=True)
        performer2 = create_performer(name="Anais Amore", gender=GenderEnum.FEMALE, favorite=False)
        performer3 = create_performer(name="Jay Bangher", gender=GenderEnum.MALE)

        performers = [performer1, performer2, performer3]

        field_settings = PerformerFieldSettings.model_validate(
            {
                "separator": ", ",
                "sort_by": ["favorite", "name"],
                "limit": 3,
                "limit_exceeded_behavior": "keep",
                "exclude_genders": ["MALE"],
            }
        )

        expected = "Mandy Muse, Anais Amore"
        actual = format_performers_field(performers=performers, settings=field_settings)

        assert expected == actual

    def test_performers_are_sorted_before_limit_is_applied(self):
        performer1 = create_performer(rating100=100)
        performer2 = create_performer(rating100=90)
        performer3 = create_performer(rating100=80)
        performer4 = create_performer(rating100=70)

        performers = [performer1, performer2, performer3, performer4]

        settings = PerformerFieldSettings.model_validate(
            {
                "separator": ", ",
                "sort_by": ["rating"],
                "limit": 2,
            }
        )

        # performer1 should be first since it has the highest rating
        # If performers limit is applied before it is sorted by rating, performer1 may be discarded
        # - that is not expected behavior

        expected = f"{performer1.name}, {performer2.name}"
        actual = format_performers_field(performers=performers, settings=settings)

        assert expected == actual

        # reverse the performer order and ensure the result is the same

        expected = expected
        actual = format_performers_field(performers=list(reversed(performers)), settings=settings)

        assert expected == actual

    def test_performers_are_filtered_before_limit_is_applied(self):
        performer1 = create_performer(gender=GenderEnum.FEMALE)
        performer2 = create_performer(gender=GenderEnum.MALE)
        performer3 = create_performer(gender=GenderEnum.MALE)
        performer4 = create_performer(gender=GenderEnum.MALE)

        performers = [performer1, performer2, performer3, performer4]

        settings = PerformerFieldSettings.model_validate(
            {
                "separator": ", ",
                "exclude_genders": ["MALE"],
                "limit": 1,
            }
        )

        # performer1 should be in the result since they are female
        # If performers limit is applied before it is filtered, performer1 may be discarded
        # - that is not expected behavior

        expected = f"{performer1.name}"
        actual = format_performers_field(performers=performers, settings=settings)

        assert expected == actual

        # reverse the performer order and ensure the result is the same

        expected = expected
        actual = format_performers_field(performers=list(reversed(performers)), settings=settings)

        assert expected == actual
