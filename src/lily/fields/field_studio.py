from string import Template
from typing import Optional

from lily.fields.common import TextReplacementSetting, apply_text_replacements
from lily.helpers.validate_template import validate_template_identifiers
from lily.models.core import BaseModelWithExactAttributes
from lily.models.stash_graphql_models.studio import Studio
from lily.stash_context import StashContext


class StudioFieldSettings(BaseModelWithExactAttributes):
    template: str = "${studio}"
    squeeze_name: bool = False
    replacements: Optional[list[TextReplacementSetting]] = None


def studio_field(stash_context: StashContext, settings: StudioFieldSettings) -> str:
    studio_field_str = format_studio_field(stash_context.scene.studio, settings)
    studio_field_str = apply_text_replacements(studio_field_str, settings.replacements)

    return studio_field_str


def format_studio_field(studio: Optional[Studio], settings: StudioFieldSettings) -> str:
    if studio is None:
        return ""

    formatted_studio_name = format_studio_name(studio, settings.squeeze_name)

    return template_studio_name(formatted_studio_name, settings.template)


def template_studio_name(studio_name: str, studio_template: str) -> str:
    validate_template_identifiers(studio_template, ["studio"])

    return Template(studio_template).safe_substitute(studio=studio_name)


def format_studio_name(studio: Studio, squeeze_studio_name: bool) -> str:
    if squeeze_studio_name:
        return studio.name.replace(" ", "")

    return str(studio.name)
