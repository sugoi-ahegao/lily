from lily.models.core import BaseModelWithExactAttributes


class PathSettings(BaseModelWithExactAttributes):
    max_path_length: int = 250
    field_removal_order: list[str] = []
    duplicate_suffix_template: str = " (${num})"
    prevent_consecutive_nested_dirs: bool = False


class PostTemplatingFileNameSettings(BaseModelWithExactAttributes):
    whitespace_character: str = " "


class PostTemplatingSettings(BaseModelWithExactAttributes):
    path: PathSettings = PathSettings()
    file_name: PostTemplatingFileNameSettings = PostTemplatingFileNameSettings()
