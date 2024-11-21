from lily.models.core import BaseModelWithExactAttributes


class PathSettings(BaseModelWithExactAttributes):
    max_path_length: int = 250
    field_removal_order: list[str] = []
    duplicate_suffix_template: str = " (${num})"


class PostTemplatingSettings(BaseModelWithExactAttributes):
    path: PathSettings = PathSettings()
