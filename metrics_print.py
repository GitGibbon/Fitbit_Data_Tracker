

def print_exercise_metrics(exercise_data):
    print("\n=== Exercise Metrics ===")
    if not exercise_data:
        print("  No exercise recorded for this period.")
        return
    for ex in exercise_data:
        interval = ex["exercise"]["interval"]
        metrics = ex["exercise"]["metricsSummary"]
        zones = metrics["heartRateZoneDurations"]

        # Convert values
        active_duration_min = int(ex["exercise"]["activeDuration"].replace("s", "")) / 60
        distance_m = metrics["distanceMillimeters"] / 1000

        print("\nExercise Session:")
        print(f"  Start Time (UTC): {interval['startTime']}")
        print(f"  End Time   (UTC): {interval['endTime']}")
        print(f"  Active Duration: {active_duration_min:.1f} minutes")
        print(f"  Calories Burned: {metrics['caloriesKcal']} kcal")
        print(f"  Distance: {distance_m:.2f} meters")
        print(f"  Steps: {metrics['steps']}")
        print(f"  Avg Heart Rate: {metrics['averageHeartRateBeatsPerMinute']} bpm")
        print(f"  Active Zone Minutes: {metrics['activeZoneMinutes']}")

        print("  Heart Rate Zones:")
        print(f"    Light: {zones['lightTime']}")
        print(f"    Moderate: {zones['moderateTime']}")
        print(f"    Vigorous: {zones['vigorousTime']}")
        print(f"    Peak: {zones['peakTime']}")


def print_sleep_metrics(sleep_data):
    print("\n=== Sleep Metrics ===")
    if not sleep_data:
        print("  No sleep recorded for this period.")
        return
    for sl in sleep_data:
        interval = sl["sleep"]["interval"]
        summary = sl["sleep"]["summary"]
        stages = summary["stagesSummary"]

        print("\nSleep Session:")
        print(f"  Start Time (UTC): {interval['startTime']}")
        print(f"  End Time   (UTC): {interval['endTime']}")
        print(f"  Total Duration: {summary['minutesInSleepPeriod']} minutes")
        print(f"  Minutes Asleep: {summary['minutesAsleep']}")
        print(f"  Minutes Awake: {summary['minutesAwake']}")

        print("  Sleep Stages:")
        for stage in stages:
            print(f"    {stage['type']}: {stage['minutes']} minutes (count: {stage['count']})")


def print_steps_metrics(steps_rollup):
    print("\n=== Steps Metrics ===")
    points = steps_rollup.get("rollupDataPoints", [])
    if not points:
        print("  No steps recorded for this period.")
        return

    for dp in points:
        d = dp["civilStartTime"]["date"]
        total_steps = int(dp["steps"]["countSum"])
        print(f"\nSteps Summary ({d['year']}-{d['month']:02d}-{d['day']:02d}):")
        print(f"  Total Steps: {total_steps}")


def print_calories_metrics(calories_rollup):
    print("\n=== Calories Metrics ===")
    points = calories_rollup.get("rollupDataPoints", [])
    if not points:
        print("  No calories recorded for this period.")
        return

    for dp in points:
        d = dp["civilStartTime"]["date"]
        kcal = dp["totalCalories"]["kcalSum"]
        print(f"\nCalories Summary ({d['year']}-{d['month']:02d}-{d['day']:02d}):")
        print(f"  Total Calories: {kcal:.0f} kcal")


def print_heart_rate_metrics(heart_rate_rollup):
    print("\n=== Heart Rate Metrics ===")
    points = heart_rate_rollup.get("rollupDataPoints", [])
    if not points:
        print("  No heart rate recorded for this period.")
        return

    for dp in points:
        d = dp["civilStartTime"]["date"]
        hr = dp["heartRate"]
        print(f"\nHeart Rate Summary ({d['year']}-{d['month']:02d}-{d['day']:02d}):")
        print(f"  Average: {hr['beatsPerMinuteAvg']:.0f} bpm")
        print(f"  Min: {hr['beatsPerMinuteMin']} bpm")
        print(f"  Max: {hr['beatsPerMinuteMax']} bpm")