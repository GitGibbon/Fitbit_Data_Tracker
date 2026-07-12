import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os

# Each data type allows different filterable fields, so map per type.
# We are using local (civil) time for filtering, so we can get the data for a specific day in our timezone.
_FILTER_FIELD = {
    "exercise": "exercise.interval.civil_start_time",
    "sleep": "sleep.interval.civil_end_time",
}

def get_data(access_token, point):
    tz = ZoneInfo(os.getenv("TIME_ZONE"))
    day = (datetime.now(tz) - timedelta(days=1)).date()   # activity day D (yesterday)
    field = _FILTER_FIELD[point]

    #Our exercise happened during day D, but we want the exercise before our night of rest.
    #This means we need to exclude sleep from the rest of the data.
    #We do this by setting the lower bound to the next day for sleep, and the same day for everything else.
    if point == "sleep":
        lo = day + timedelta(days=1)
    else:
        lo = day
    hi = lo + timedelta(days=1)

    url = f"https://health.googleapis.com/v4/users/me/dataTypes/{point}/dataPoints"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    params = {
        "filter": f'{field} >= "{lo}T00:00:00" AND {field} < "{hi}T00:00:00"'
    }
    try:
        ask = requests.get(url, headers=headers, params=params, timeout=10)
        ask.raise_for_status()
    except requests.exceptions.HTTPError:
        raise RuntimeError(f"HTTP error occurred: {ask.status_code} - {ask.text}")
    response = ask.json()
    return response.get("dataPoints", [])


def get_daily_rollup(access_token, point, days_ago=1):
    #Google returns steps per minute, so daily rollup allows us to ask for the result as the amount from a whole day, instead fo summing thousands of steps.
    time_zone = os.getenv("TIME_ZONE")
    tz = ZoneInfo(time_zone)
    day = (datetime.now(tz) - timedelta(days=days_ago)).date()
    next_day = day + timedelta(days=1)
    # dailyRollUp uses civil time in order to most accurately map specific days to their sleep and activity schedules.
    #tz is ONLY used for identifying the calendar day, do not use it for another purpose or translate it.
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
    try:
        ask = requests.post(url, headers=headers, json=body, timeout=10)
        ask.raise_for_status()
    except requests.exceptions.HTTPError:
        raise RuntimeError(f"HTTP error occurred: {ask.status_code} - {ask.text}")
    response = ask.json()
    return response
