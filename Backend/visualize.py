import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).parent

HISTORY_FILE = BASE_DIR / "data" / "processed_solar_weather_dataset.csv"
PREDICTION_FILE = BASE_DIR / "outputs" / "solar_predictions.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
GRAPH_FILE = OUTPUT_DIR / "solar_prediction_graph.png"


def create_visualization():
    history = pd.read_csv(HISTORY_FILE, parse_dates=["timestamp"])
    predictions = pd.read_csv(
        PREDICTION_FILE,
        parse_dates=["timestamp"]
    )

    # Show the last 14 days of historical solar output.
    last_timestamp = history["timestamp"].max()
    history = history[
        history["timestamp"] >= last_timestamp - pd.Timedelta(days=14)
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(14, 6))

    plt.plot(
        history["timestamp"],
        history["solar_output"],
        label="Historical Solar Output",
        linewidth=1.5,
    )

    plt.plot(
        predictions["timestamp"],
        predictions["predicted_solar_output"],
        label="Predicted Solar Output",
        linewidth=2,
    )

    plt.axvline(
        predictions["timestamp"].min(),
        linestyle="--",
        label="Forecast Start",
    )

    plt.title("Pune Solar Power: Historical and Predicted Output")
    plt.xlabel("Timestamp")
    plt.ylabel("Solar Output (arbitrary units)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig(GRAPH_FILE, dpi=150)
    plt.close()

    print("Visualization created successfully!")
    print(f"Graph saved to: {GRAPH_FILE}")
    print("\nFuture prediction table:")
    print(predictions.to_string(index=False))


if __name__ == "__main__":
    create_visualization()