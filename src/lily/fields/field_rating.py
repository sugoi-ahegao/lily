from string import Template
from typing import Optional

from lily.fields.common import TextReplacementSetting, apply_text_replacements
from lily.helpers.validate_template import validate_template_identifiers
from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class RatingFieldSettings(BaseModelWithExactAttributes):
    template: str = "${rating}"
    replacements: Optional[list[TextReplacementSetting]] = None


def rating_field(stash_context: StashContext, settings: RatingFieldSettings) -> str:
    rating_field_str = format_rating_field(stash_context.scene.rating100, settings)
    rating_field_str = apply_text_replacements(rating_field_str, settings.replacements)

    return rating_field_str


def format_rating_field(rating: Optional[int], field_settings: RatingFieldSettings) -> str:
    validate_template_identifiers(field_settings.template, ["rating"])

    if rating is None:
        return ""

    return Template(field_settings.template).safe_substitute(rating=rating)
