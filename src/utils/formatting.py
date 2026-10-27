from datetime import datetime
from gettext import gettext as _
from gi.repository import GLib


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
    g_dt = GLib.DateTime.new_from_iso8601(
        dt.isoformat(), GLib.TimeZone.new_local()
    )
    if g_dt is None:
        return dt.strftime("%Y-%m-%d %H:%M")

    now = GLib.DateTime.new_now_local()

    if _day_key(g_dt) == _day_key(now):
        return _("Today %s") % g_dt.format("%H:%M")

    if _day_key(g_dt) == _day_key(now.add_days(-1)):
        return _("Yesterday %s") % g_dt.format("%H:%M")
    return g_dt.format("%x %H:%M")


def _day_key(dt: GLib.DateTime) -> str:
    return dt.format("%Y-%m-%d")


def datetime_from_iso(timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp)


def date_with_seconds() -> str:
    return datetime.now().isoformat(timespec="seconds")
