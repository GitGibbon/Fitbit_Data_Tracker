from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

def get_yesterday():
    tz = ZoneInfo("America/Los_Angeles")
    now = datetime.now(tz)
    yesterday = now - timedelta(days=1)

    start_local = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_local = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    start_yesterday = start_local.astimezone(ZoneInfo("UTC")).isoformat()
    end_yesterday = end_local.astimezone(ZoneInfo("UTC")).isoformat()
    return start_yesterday, end_yesterday