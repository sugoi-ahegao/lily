from string import Template
from typing import Optional

from lily.fields.common import TextReplacementSetting, apply_text_replacements, satisfies_all_constraints
from lily.helpers.validate_template import validate_template_identifiers
from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class RatingFieldSettings(BaseModelWithExactAttributes):
    template: str = "${rating}"
    mappings: Optional[dict[str, str]] = None
    replacements: Optional[list[TextReplacementSetting]] = None


def rating_field(stash_context: StashContext, settings: RatingFieldSettings) -> str:
    rating_field_str = format_rating_field(stash_context.scene.rating100, settings)
    rating_field_str = apply_text_replacements(rating_field_str, settings.replacements)

    return rating_field_str


def format_rating_field(rating: Optional[int], field_settings: RatingFieldSettings) -> str:
    validate_template_identifiers(field_settings.template, ["rating"])

    if rating is None:
        return ""

    rating_text = rating

    if field_settings.mappings is not None:
        for constraints, value in field_settings.mappings.items():
            if satisfies_all_constraints(rating, constraints):
                rating_text = value
                break

    return Template(field_settings.template).safe_substitute(rating=rating_text)
