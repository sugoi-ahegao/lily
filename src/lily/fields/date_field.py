import datetime
from typing import Optional

from lily.models.core import BaseModelWithExactAttributes


class DateFieldSettings(BaseModelWithExactAttributes):
    format: str = "%Y-%m-%d"


def format_date_field(date: Optional[datetime.date], settings: DateFieldSettings) -> str:
    if date is None:
        return ""

    return date.strftime(settings.format)
