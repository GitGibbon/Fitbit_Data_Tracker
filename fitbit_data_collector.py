import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os

# Each data type allows different filterable fields (AIP-160), so map per type.
# Both use civil (wall-clock) time -- same local-day model as get_daily_rollup.
_FILTER_FIELD = {
    "exercise": "exercise.interval.civil_start_time",
    "sleep": "sleep.interval.civil_end_time",
}

def get_data(access_token, point):
    tz = ZoneInfo(os.getenv("TIME_ZONE"))
    yesterday = (datetime.now(tz) - timedelta(days=1)).date()
    today = yesterday + timedelta(days=1)
    field = _FILTER_FIELD[point]

    url = f"https://health.googleapis.com/v4/users/me/dataTypes/{point}/dataPoints"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    # Scope to yesterday's local day server-side; civil time takes no offset. Only
    # >= and < are supported operators, so use a half-open [start, next-day) window.
    params = {
        "filter": f'{field} >= "{yesterday}T00:00:00" AND {field} < "{today}T00:00:00"'
    }

    response = requests.get(url, headers=headers, params=params).json()
    if "error" in response:
        raise RuntimeError(f"Error fetching data: {response['error']}")
    # ponytail: no pagination; one local day of sleep/exercise events is far under the
    # 1440 default page size. Add pageToken handling if a day ever exceeds that.
    return response.get("dataPoints", [])


def get_daily_rollup(access_token, point, days_ago=1):
    #Google returns steps per minute, so daily rollup allows us to ask for the result as the amount from a whole day, instead fo summing thousands of steps.
    time_zone = os.getenv("TIME_ZONE")
    tz = ZoneInfo(time_zone)
    day = (datetime.now(tz) - timedelta(days=days_ago)).date()
    next_day = day + timedelta(days=1)
    # dailyRollUp uses CivilTimeInterval (wall-clock), which has no timezone field by
    # design. tz is only used above to pick which calendar day "yesterday" is. Do NOT
    # convert this range to UTC — that would feed physical time into a civil-time field.

    url = f"https://health.googleapis.com/v4/users/me/dataTypes/{point}/dataPoints:dailyRollUp"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    body = {
        "range": {
            "start": {
                "date": {"year": day.year, "month": day.month, "day": day.day},
                "time": {"hours": 0, "minutes": 0},
            },
            "end": {
                "date": {"year": next_day.year, "month": next_day.month, "day": next_day.day},
                "time": {"hours": 0, "minutes": 0},
            },
        },
        "windowSizeDays": 1,
    }

    response = requests.post(url, headers=headers, json=body).json()
    if "error" in response:
        raise RuntimeError(f"Error rolling up {point}: {response['error']}")
    return response
