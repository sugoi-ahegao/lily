from string import Template
from typing import Optional

from lily.helpers.validate_template import validate_template_identifiers
from lily.models.core import BaseModelWithExactAttributes
from lily.models.stash_graphql_models.studio import Studio


class StudioFieldSettings(BaseModelWithExactAttributes):
    template: str = "${studio}"
    squeeze_name: bool = False


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
