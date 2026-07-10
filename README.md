# Fitbit Data Tracker

A Python tool that pulls daily health metrics from a Fitbit device via the
[Google Health API](https://developers.google.com/health) (the next generation
of the Fitbit Web API) and prints a clean daily summary.

## Metrics collected

For a given day it reports:

- **Sleep** — duration, minutes asleep/awake, and a breakdown of sleep stages
- **Steps** — daily total
- **Exercise** — logged workout sessions (duration, calories, distance, heart-rate zones)
- **Calories** — total energy burned (kcal)
- **Heart rate** — daily average, min, and max (bpm)

## How it works

- Refreshes a short-lived OAuth access token from a stored refresh token.
- Fetches per-event data (sleep, exercise) with the `list` endpoint and filters by date.
- Fetches daily aggregates (steps, calories, heart rate) with the `dailyRollUp`
  endpoint, so it gets a correct daily total instead of summing thousands of
  per-minute samples.

## Setup

1. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with your Google Health API credentials:

   ```
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   GOOGLE_REFRESH_TOKEN=your_refresh_token
   ```

   `.env` is gitignored and never committed.

3. Run it:

   ```bash
   python main.py
   ```

## Roadmap

- [ ] Persist daily metrics to a SQLite database
- [ ] Query trends over time (e.g. weekly sleep and step averages)
- [ ] Add basic error handling for network/API failures
- [ ] Add regression and a messaging system for AI driven insights on your specific sleep schedule and what works best for you