from string import Template
from typing import Optional, Self

from pydantic import model_validator

from lily.fields.model_field_settings import FieldSettings, field_registry_file_dir, field_registry_file_name
from lily.filters.model_filter_settings import FilterSettings
from lily.models.core import BaseModelWithExactAttributes
from lily.models.user_settings.post_templating_settings import PostTemplatingSettings


class RenameRule(BaseModelWithExactAttributes):
    name: Optional[str] = None
    template_file_dir: str
    template_file_name: str

    filters: FilterSettings = FilterSettings()
    field_settings: FieldSettings = FieldSettings()
    post_templating_settings: PostTemplatingSettings = PostTemplatingSettings()

    @model_validator(mode="after")
    def validate_template_file_dir(self) -> Self:
        for field_name in Template(self.template_file_dir).get_identifiers():
            if field_name not in field_registry_file_dir:
                raise ValueError(f"Unknown field found in file dir template: '{field_name}'")

        return self

    @model_validator(mode="after")
    def validate_template_file_name(self) -> Self:
        for field_name in Template(self.template_file_name).get_identifiers():
            if field_name not in field_registry_file_name:
                raise ValueError(f"Unknown field found in file name template: '{field_name}'")

        return self
