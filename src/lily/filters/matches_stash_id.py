from typing import Optional, Self

from pydantic import model_validator

from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class MatchesStashIDFilterSettings(BaseModelWithExactAttributes):
    value: Optional[str] = None
    not_null: Optional[bool] = None

    @model_validator(mode="after")
    def require_value_xor_not_null(self) -> Self:
        if (self.value is None) and (self.not_null is None):
            raise ValueError("Either 'value' or 'not_null' is required")

        if (self.value is not None) and (self.not_null is not None):
            raise ValueError("Both 'value' and 'not_null' cannot be set")

        return self


def matches_stash_id(stash_context: StashContext, settings: MatchesStashIDFilterSettings) -> bool:
    if settings.not_null is not None:
        if settings.not_null is True:
            return len(stash_context.scene.stash_ids) > 0

        if settings.not_null is False:
            return len(stash_context.scene.stash_ids) == 0

    assert settings.value is not None, "This should have been caught by the model validator"

    # Extract stash id strings from the stash id models to compare values
    stash_ids = [stash_id.stash_id for stash_id in stash_context.scene.stash_ids]

    return settings.value in stash_ids
