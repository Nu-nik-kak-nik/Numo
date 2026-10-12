from datetime import datetime
from gettext import gettext as _


def format_duration(seconds: float) -> str:
    total = int(seconds)
    minutes, secs = divmod(total, 60)
    return f"{minutes}:{secs:02d}"


def format_duration_with_hours(seconds: float) -> str:
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}"


def format_timestamp(dt: datetime) -> str:
    now = datetime.now()
    if dt.date() == now.date():
        return _("Today %s") % dt.strftime("%H:%M")
    return dt.strftime("%Y-%m-%d %H:%M")
