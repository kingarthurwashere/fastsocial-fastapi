from datetime import datetime
from zoneinfo import ZoneInfo

def now_tz(tz_name: str) -> datetime:
    return datetime.now(ZoneInfo(tz_name))

def today_iso(tz_name: str) -> str:
    dt = now_tz(tz_name)
    return dt.strftime("%Y-%m-%d")
