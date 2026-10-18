
import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("WEATHER_API_KEY")
FORECAST_URL = "https://api.weatherapi.com/v1/forecast.json"

DEFAULT_LOCATION = "Pune, Maharashtra, India"


def fetch_weather_forecast(hours=48, location=DEFAULT_LOCATION):
    if not API_KEY:
        raise ValueError(
            "WEATHER_API_KEY missing hai. Backend/.env check karo."
        )

    location = str(location).strip()

    if not location:
        location = DEFAULT_LOCATION

    response = requests.get(
        FORECAST_URL,
        params={
            "key": API_KEY,
            "q": location,
            "days": 3,
            "aqi": "no",
            "alerts": "no",
        },
        timeout=20,
    )

    response.raise_for_status()
    data = response.json()

    if "forecast" not in data:
        raise ValueError("Weather API response mein forecast nahi mila.")

    hourly_data = []

    for day in data["forecast"]["forecastday"]:
        for hour in day["hour"]:
            timestamp = pd.to_datetime(
                hour["time"],
                errors="coerce",
            )

            if pd.isna(timestamp):
                continue

            wind_kph = hour.get("wind_kph")

            hourly_data.append({
                "timestamp": timestamp,
                "temperature": hour.get("temp_c"),
                "humidity": hour.get("humidity"),
                "cloud_cover": hour.get("cloud"),
                "wind_speed": (
                    wind_kph / 3.6
                    if wind_kph is not None
                    else None
                ),
                "precipitation": hour.get("precip_mm"),
            })

    df = pd.DataFrame(hourly_data)

    if df.empty:
        raise ValueError("Weather API se hourly forecast nahi mila.")

    df = (
        df.drop_duplicates(subset="timestamp")
        .sort_values("timestamp")
        .reset_index(drop=True)
    )

    # Use the selected location's local timezone.
    location_timezone = data.get("location", {}).get(
        "tz_id", "Asia/Kolkata"
    )

    now = pd.Timestamp.now(tz=location_timezone).tz_localize(None)

    df = df[df["timestamp"] >= now].head(hours).copy()

    if df.empty:
        raise ValueError(
            f"{location} ke liye future hourly forecast nahi mila."
        )

    if len(df) < hours:
        print(
            f"Warning: API ne sirf {len(df)} future hourly records diye."
        )

    weather_columns = [
        "temperature",
        "humidity",
        "cloud_cover",
        "wind_speed",
        "precipitation",
    ]

    df[weather_columns] = df[weather_columns].interpolate(
        limit_direction="both"
    )

    if df[weather_columns].isna().any().any():
        raise ValueError(
            "Weather forecast mein kuch fields missing hain."
        )

    return df.reset_index(drop=True)


if __name__ == "__main__":
    try:
        forecast = fetch_weather_forecast(
            hours=48,
            location="Pune, Maharashtra, India",
        )

        print("Weather forecast fetched successfully!")
        print(f"Forecast records: {len(forecast)}")
        print(forecast.head())

    except requests.RequestException as error:
        print(f"Weather API request failed: {error}")

    except (ValueError, KeyError) as error:
        print(f"Weather forecast error: {error}")
