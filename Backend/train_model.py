import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "processed_solar_weather_dataset.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_FILE = MODEL_DIR / "solar_model.joblib"
METRICS_FILE = MODEL_DIR / "model_metrics.json"

FEATURES = [
    "temperature",
    "humidity",
    "cloud_cover",
    "wind_speed",
    "precipitation",
    "hour_sin",
    "hour_cos",
    "day_of_week",
    "is_weekend",
]

TARGET = "solar_output"


def train_model():
    df = pd.read_csv(DATA_FILE, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    # First 50 days for training, last 10 days for validation.
    split_index = 50 * 24

    train_df = df.iloc[:split_index]
    validation_df = df.iloc[split_index:]

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_val = validation_df[FEATURES]
    y_val = validation_df[TARGET]

    # Tune a small set of hyperparameters using chronological folds.
    time_cv = TimeSeriesSplit(n_splits=3)

    parameter_grid = {
        "n_estimators": [100, 200],
        "max_depth": [None, 15],
        "min_samples_leaf": [1, 2],
    }

    search = GridSearchCV(
        estimator=RandomForestRegressor(
            random_state=42,
            n_jobs=-1,
        ),
        param_grid=parameter_grid,
        scoring="neg_mean_absolute_error",
        cv=time_cv,
        n_jobs=-1,
    )

    search.fit(X_train, y_train)
    model = search.best_estimator_

    predictions = np.clip(model.predict(X_val), 0, None)

    mae = mean_absolute_error(y_val, predictions)
    rmse = np.sqrt(mean_squared_error(y_val, predictions))
    r2 = r2_score(y_val, predictions)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Save model and feature schema for future predictions.
    joblib.dump(
        {
            "model": model,
            "features": FEATURES,
        },
        MODEL_FILE,
    )

    metrics = {
        "model": "RandomForestRegressor",
        "training_rows": len(train_df),
        "validation_rows": len(validation_df),
        "training_start": str(train_df["timestamp"].min()),
        "training_end": str(train_df["timestamp"].max()),
        "validation_start": str(validation_df["timestamp"].min()),
        "validation_end": str(validation_df["timestamp"].max()),
        "best_parameters": search.best_params_,
        "validation_MAE": float(mae),
        "validation_RMSE": float(rmse),
        "validation_R2": float(r2),
    }

    with open(METRICS_FILE, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4)

    print("Model training completed successfully!")
    print(f"Training rows: {len(train_df)}")
    print(f"Validation rows: {len(validation_df)}")
    print(f"Best parameters: {search.best_params_}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²: {r2:.4f}")
    print(f"Saved model: {MODEL_FILE}")
    print(f"Saved metrics: {METRICS_FILE}")


if __name__ == "__main__":
    train_model()