from enum import Enum
from typing import Optional

from lily.models.core import BaseModelWithExactAttributes


class Capitalization(str, Enum):
    LOWERCASE = "lowercase"
    UPPERCASE = "uppercase"
    TITLE = "title"


class TitleFieldSettings(BaseModelWithExactAttributes):
    capitalization: Optional[Capitalization] = None


def format_title_field(title: Optional[str], settings: TitleFieldSettings) -> str:
    if title is None:
        return ""

    if settings.capitalization == Capitalization.LOWERCASE:
        return title.lower()

    if settings.capitalization == Capitalization.UPPERCASE:
        return title.upper()

    if settings.capitalization == Capitalization.TITLE:
        return title.title()

    return title
