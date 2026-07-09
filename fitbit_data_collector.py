import requests
import json
from get_yesterday import get_yesterday
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

start, end = get_yesterday()
start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))

def get_data(access_token, point):
    url = f"https://health.googleapis.com/v4/users/me/dataTypes/{point}/dataPoints"
    #like the subject like, who are you and how do you want your data back?
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers).json()
    if "error" in response:
        raise RuntimeError(f"Error fetching data: {response['error']}")
    results = []
    for dp in response.get("dataPoints", []):
        interval = dp[point]["interval"]
        et = datetime.fromisoformat(interval["endTime"].replace("Z", "+00:00"))
        if start_dt <= et <= end_dt:
            results.append(dp)


    return results


def get_daily_rollup(access_token, point, days_ago=1):
    # dailyRollUp is a POST that asks the server for one total per civil day,
    # so we don't have to fetch and sum thousands of per-minute data points.
    tz = ZoneInfo("America/Los_Angeles")
    day = (datetime.now(tz) - timedelta(days=days_ago)).date()
    next_day = day + timedelta(days=1)

    url = f"https://health.googleapis.com/v4/users/me/dataTypes/{point}/dataPoints:dailyRollUp"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    # range is a closed-open interval [start, end) of civil (local) dates.
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
