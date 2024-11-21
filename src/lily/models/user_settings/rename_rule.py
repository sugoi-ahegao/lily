from typing import Optional

from lily.models.core import BaseModelWithExactAttributes
from lily.models.user_settings.field_settings import FieldSettings
from lily.models.user_settings.filter_settings import FilterSettings
from lily.models.user_settings.post_templating_settings import PostTemplatingSettings


class RenameRule(BaseModelWithExactAttributes):
    name: Optional[str] = None
    template_file_dir: str
    template_file_name: str

    filters: FilterSettings = FilterSettings()
    field_settings: FieldSettings = FieldSettings()
    post_templating_settings: PostTemplatingSettings = PostTemplatingSettings()
