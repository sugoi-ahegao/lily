from string import Template

from lily.helpers.validate_template import validate_template_identifiers
from lily.models.core import BaseModelWithExactAttributes
from lily.models.stash_graphql_models.scene import Scene


class RatingFieldSettings(BaseModelWithExactAttributes):
    template: str = "${rating}"


def format_rating_field(scene: Scene, field_settings: RatingFieldSettings) -> str:
    validate_template_identifiers(field_settings.template, ["rating"])

    if scene.rating100 is None:
        return ""

    return Template(field_settings.template).safe_substitute(rating=scene.rating100)
