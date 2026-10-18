import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "data" / "solar_weather_dataset.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed_solar_weather_dataset.csv"

WEATHER_COLUMNS = [
    "temperature",
    "humidity",
    "cloud_cover",
    "wind_speed",
    "precipitation",
]

TARGET_COLUMN = "solar_output"


def add_time_features(df):
    """Create reusable time-based features."""
    df = df.copy()

    hour = df["timestamp"].dt.hour
    day_of_week = df["timestamp"].dt.dayofweek

    df["hour"] = hour
    df["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    df["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    df["day_of_week"] = day_of_week
    df["is_weekend"] = (day_of_week >= 5).astype(int)

    return df


def load_and_clean_data():
    df = pd.read_csv(INPUT_FILE)

    # Parse timestamps and remove invalid timestamps.
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )
    df = df.dropna(subset=["timestamp"])

    # Sort timestamps and handle duplicate records.
    df = (
        df.sort_values("timestamp")
        .drop_duplicates(subset="timestamp", keep="last")
        .set_index("timestamp")
    )

    numeric_columns = WEATHER_COLUMNS + [TARGET_COLUMN]

    # Convert invalid numeric values to NaN.
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Restore any missing hourly timestamps.
    hourly_index = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="h",
    )
    df = df.reindex(hourly_index)
    df.index.name = "timestamp"

 
    # Handle physically impossible weather values first.
    valid_ranges = {
        "temperature": (-50, 60),
        "humidity": (0, 100),
        "cloud_cover": (0, 100),
        "wind_speed": (0, 100),
        "precipitation": (0, None),
        "solar_output": (0, None),
    }

    for column, (lower, upper) in valid_ranges.items():
        df[column] = df[column].clip(
            lower=lower, upper=upper
        )

    # Handle statistical outliers using the IQR method.
    # Extreme observations are treated as missing and interpolated.
    outlier_columns = WEATHER_COLUMNS + [TARGET_COLUMN]

    for column in outlier_columns:
        values = df[column].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_mask = (
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        )

        df.loc[outlier_mask, column] = np.nan

    # Fill missing values using time interpolation.
    for column in numeric_columns:
        df[column] = df[column].interpolate(
            method="time", limit_direction="both"
        )

    # Fallback for columns that remain entirely missing.
    for column in numeric_columns:
        if df[column].isna().any():
            df[column] = df[column].fillna(0)


    df = df.reset_index()
    df = add_time_features(df)

    df.to_csv(OUTPUT_FILE, index=False)

    print("Data processing completed successfully!")
    print(f"Rows after cleaning: {len(df)}")
    print(f"Missing values remaining: {int(df.isna().sum().sum())}")
    print(f"Processed file: {OUTPUT_FILE}")
    print("\nFirst five rows:")
    print(df.head())


if __name__ == "__main__":
    load_and_clean_data()