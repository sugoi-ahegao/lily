from enum import Enum
from typing import Optional

from lily.fields.common import TextReplacementSetting, apply_text_replacements
from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class Capitalization(str, Enum):
    LOWERCASE = "lowercase"
    UPPERCASE = "uppercase"
    TITLE = "title"


class TitleFieldSettings(BaseModelWithExactAttributes):
    capitalization: Optional[Capitalization] = None
    remove_prefixes: Optional[list[str]] = None
    fallback_to_source_video_file_name: bool = False
    replacements: Optional[list[TextReplacementSetting]] = None


def title_field(stash_context: StashContext, settings: TitleFieldSettings) -> str:
    if settings.fallback_to_source_video_file_name:
        scene_title = stash_context.scene.title

        if scene_title is None or scene_title.strip() == "":
            return stash_context.video_file.path.stem

    title_field_str = format_title_field(stash_context.scene.title, settings)
    title_field_str = apply_text_replacements(title_field_str, settings.replacements)

    return title_field_str


def format_title_field(title: Optional[str], settings: TitleFieldSettings) -> str:
    if title is None:
        return ""

    if settings.remove_prefixes is not None:
        for prefix in settings.remove_prefixes:
            title = title.removeprefix(prefix)
            # Remove any whitespace that might have been left behind
            title = title.lstrip()

    if settings.capitalization == Capitalization.LOWERCASE:
        return title.lower().strip()

    if settings.capitalization == Capitalization.UPPERCASE:
        return title.upper().strip()

    if settings.capitalization == Capitalization.TITLE:
        return title.title().strip()

    return title.strip()
