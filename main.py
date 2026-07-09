import os
from dotenv import load_dotenv
from fitbit_access_call import refresh_access_token
from fitbit_data_collector import get_data, get_daily_rollup
from metrics_print import (
    print_exercise_metrics,
    print_sleep_metrics,
    print_steps_metrics,
    print_calories_metrics,
    print_heart_rate_metrics,
)

load_dotenv()

client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

with open("secret.txt", "r") as f:
    refresh_token = f.read().strip()

access_token = refresh_access_token(refresh_token, client_id, client_secret)
exercise_data = get_data(access_token, "exercise")
steps_rollup = get_daily_rollup(access_token, "steps")
sleep_data = get_data(access_token, "sleep")
calories_rollup = get_daily_rollup(access_token, "total-calories")
heart_rate_rollup = get_daily_rollup(access_token, "heart-rate")

print_exercise_metrics(exercise_data)
print_steps_metrics(steps_rollup)
print_sleep_metrics(sleep_data)
print_calories_metrics(calories_rollup)
print_heart_rate_metrics(heart_rate_rollup)

