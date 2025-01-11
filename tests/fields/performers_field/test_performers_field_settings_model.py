from typing import Any

import pytest
from pydantic import ValidationError
from tests.testing_utils.generic import generic

from lily.fields.field_performers import (
    PerformerFieldSettings,
    PerformerLimitExceededBehavior,
    PerformerSortKey,
)
from lily.models.stash_graphql_models.performer import GenderEnum


class TestPerformersFieldSettingsModel:
    def test_performer_field_settings(self):
        # test minimal settings
        field_settings_dict: dict[str, Any] = {}

        assert PerformerFieldSettings.model_validate(field_settings_dict)

        # test all settings
        field_settings_dict = {
            "separator": ", ",
            "sort_by": ["favorite", "rating", "name"],
            "limit": 3,
            "limit_exceeded_behavior": "keep",
            "exclude_genders": ["MALE"],
        }

        assert PerformerFieldSettings.model_validate(field_settings_dict)

        # test invalid sort by key
        field_settings_dict: dict[str, Any] = {"sort_by": ["something invalid"]}

        with pytest.raises(ValidationError):
            assert PerformerFieldSettings.model_validate(field_settings_dict)

        # test limit exceeded_behavior - keep
        field_settings_dict: dict[str, Any] = {"sort_by": ["id"], "limit_exceeded_behavior": "keep"}

        assert PerformerFieldSettings.model_validate(field_settings_dict)

        # test limit exceeded_behavior - discard
        field_settings_dict: dict[str, Any] = {"sort_by": ["id"], "limit_exceeded_behavior": "discard"}

        assert PerformerFieldSettings.model_validate(field_settings_dict)

    def test_random_field_settings(self):
        assert PerformerFieldSettings.model_validate(
            {
                "separator": generic.random.generate_string_by_mask("@@"),
                "sort_by": [
                    generic.random.choice_enum_item(PerformerSortKey) for _ in range(generic.random.randint(1, 4))
                ],
                "limit": generic.random.randint(1, 3),
                "limit_exceeded_behavior": generic.random.choice_enum_item(PerformerLimitExceededBehavior),
                "exclude_genders": [
                    generic.random.choice_enum_item(GenderEnum) for _ in range(generic.random.randint(1, 4))
                ],
            }
        )
