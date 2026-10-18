
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from predict import generate_predictions
from weather_api import DEFAULT_LOCATION

app = FastAPI(title="Solar Power Prediction API")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "processed_solar_weather_dataset.csv"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://solar-power-prediction-application.vercel.app",
        "https://solar-power-prediction-application-h6so95n56.vercel.app",
        "https://solar-power-prediction-application-grfinzevi.vercel.app",
        "https://solar-power-predicti-git-5d0d24-captain-jack-sparrow-s-projects.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {"message": "Solar Power Prediction API is running"}


@app.get("/api/history")
def get_history():
    try:
        df = pd.read_csv(DATA_FILE)
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        )
        df["solar_output"] = pd.to_numeric(
            df["solar_output"], errors="coerce"
        )
        df = df.dropna(subset=["timestamp", "solar_output"])
        df = df.sort_values("timestamp").tail(336)
        df = df[["timestamp", "solar_output"]].copy()
        df["timestamp"] = df["timestamp"].dt.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        return df.to_dict(orient="records")

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to load historical data: {error}",
        )


@app.get("/api/predictions")
def get_predictions(
    location: str = Query(default=DEFAULT_LOCATION, min_length=1, max_length=150)
):
    try:
        result = generate_predictions(
            location=location.strip(),
            hours=48,
        )
        return result.to_dict(orient="records")

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to generate predictions for '{location}': {error}",
        )
