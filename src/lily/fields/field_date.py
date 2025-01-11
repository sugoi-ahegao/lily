import datetime
from typing import Optional

from lily.models.core import BaseModelWithExactAttributes
from lily.stash_context import StashContext


class DateFieldSettings(BaseModelWithExactAttributes):
    format: str = "%Y-%m-%d"


def date_field(stash_context: StashContext, settings: DateFieldSettings) -> str:
    return format_date_field(stash_context.scene.date, settings)


def format_date_field(date: Optional[datetime.date], settings: DateFieldSettings) -> str:
    if date is None:
        return ""

    return date.strftime(settings.format)
