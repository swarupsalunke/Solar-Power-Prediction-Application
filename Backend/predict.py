
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from data_processing import add_time_features
from weather_api import fetch_weather_forecast, DEFAULT_LOCATION


BASE_DIR = Path(__file__).parent
MODEL_FILE = BASE_DIR / "models" / "solar_model.joblib"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "solar_predictions.csv"


def generate_predictions(location=DEFAULT_LOCATION, hours=48):
    # Load the saved model and its expected feature schema.
    saved_model = joblib.load(MODEL_FILE)
    model = saved_model["model"]
    features = saved_model["features"]

    # Fetch weather for the selected location.
    weather_df = fetch_weather_forecast(
        hours=hours,
        location=location,
    )

    # Apply the same time features used during training.
    prediction_df = add_time_features(weather_df)

    # Ensure the model receives columns in the correct order.
    X_future = prediction_df[features]

    # Predict solar output and prevent negative values.
    predictions = np.clip(model.predict(X_future), 0, None)

    # Prepare the output table.
    result = pd.DataFrame({
        "timestamp": prediction_df["timestamp"],
        "predicted_solar_output": predictions,
    })

    # Include the selected location in the output.
    result["location"] = location

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    return result


if __name__ == "__main__":
    try:
        result = generate_predictions(
            location="Pune, Maharashtra, India",
            hours=48,
        )

        print("Solar predictions generated successfully!")
        print(f"Prediction records: {len(result)}")
        print(f"Output saved to: {OUTPUT_FILE}")
        print(result.head().to_string(index=False))

    except Exception as error:
        print(f"Prediction failed: {error}")
        raise
