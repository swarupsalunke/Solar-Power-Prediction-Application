
# Solar Power Prediction Application

A machine learning application that predicts solar power output using weather data. The project includes synthetic dataset generation, data preprocessing, regression model training, weather forecast integration, a FastAPI backend, and a React dashboard.

## Features

- Generate a synthetic hourly solar weather dataset.
- Clean missing values, duplicate timestamps, invalid values, and statistical outliers.
- Create time-based features for machine learning.
- Train and evaluate a Random Forest regression model.
- Fetch hourly weather forecasts for Pune using WeatherAPI.com.
- Generate solar output predictions for the next 48 hours.
- Visualize historical solar output and future predictions.
- Display prediction results in a React dashboard.
- Expose data through FastAPI REST endpoints.

## Technology Stack

### Backend
- Python
- Pandas and NumPy
- Scikit-learn
- Joblib
- Requests
- Matplotlib
- FastAPI and Uvicorn
- python-dotenv

### Frontend
- React
- Vite
- JavaScript
- Recharts
- CSS

### Weather Data
- WeatherAPI.com

## Project Structure

```text
Solar Power Prediction Application/
├── Backend/
│   ├── data/
│   │   ├── solar_weather_dataset.csv
│   │   └── processed_solar_weather_dataset.csv
│   ├── models/
│   │   ├── solar_model.joblib
│   │   └── model_metrics.json
│   ├── outputs/
│   │   ├── solar_predictions.csv
│   │   └── solar_prediction_graph.png
│   ├── venv/
│   ├── .env
│   ├── .gitignore
│   ├── generate_dataset.py
│   ├── data_processing.py
│   ├── train_model.py
│   ├── weather_api.py
│   ├── predict.py
│   ├── visualize.py
│   ├── main.py
│   └── requirements.txt
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   └── package.json
└── README.md
```

## Dataset Generation

The application generates a synthetic hourly dataset covering January 1, 2024, through February 29, 2024.

- Total records: 1,440 hourly rows
- Input weather features:
  - Temperature
  - Humidity
  - Cloud cover
  - Wind speed
  - Precipitation
- Target variable: Solar output

Run the following command from the Backend directory:

```bash
python generate_dataset.py
```

## Data Preprocessing

The preprocessing pipeline:

- Parses timestamps and removes invalid timestamps.
- Sorts records and removes duplicate timestamps.
- Converts invalid numeric values to missing values.
- Restores missing hourly timestamps.
- Handles physically impossible values.
- Detects statistical outliers using the Interquartile Range (IQR) method.
- Interpolates missing numeric values using time-based interpolation.
- Generates hour, hour sine, hour cosine, day of week, and weekend features.

Run:

```bash
python data_processing.py
```

The processed dataset is saved as:

`data/processed_solar_weather_dataset.csv`

## Model Training and Evaluation

The application uses a Random Forest Regressor. Model selection uses GridSearchCV with TimeSeriesSplit, and the final evaluation uses a chronological training and validation split.

Latest recorded evaluation metrics:

| Metric | Value |
|---|---:|
| Training records | 1,200 |
| Validation records | 240 |
| MAE | 16.51 |
| RMSE | 24.64 |
| R² | 0.9768 |

These metrics are calculated on the synthetic dataset's validation split. They should not be interpreted as measured real-world solar plant accuracy.

Run model training:

```bash
python train_model.py
```

The trained model and metrics are saved in the `models/` directory.

## Weather Forecast Integration

The application uses WeatherAPI.com to retrieve hourly weather forecast data for Pune, India.

Weather features include temperature, humidity, cloud cover, wind speed, and precipitation.

### Configure the API Key

1. Create an account at https://www.weatherapi.com/.
2. Obtain an API key from your WeatherAPI account.
3. Create a `.env` file inside the Backend directory.
4. Add your key:

```env
WEATHER_API_KEY=your_weatherapi_key
```

Replace the placeholder with your own key. Never commit the `.env` file or expose the API key publicly.

## Generate Predictions

From the Backend directory, run:

```bash
python predict.py
```

The script fetches weather forecasts, applies the trained model, clips negative predictions to zero, and saves the forecast to:

`outputs/solar_predictions.csv`

Generate the visualization with:

```bash
python visualize.py
```

The graph is saved as:

`outputs/solar_prediction_graph.png`

## Running the Backend

Open a terminal in the Backend directory.

Create and activate a virtual environment if needed:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the `.env` file before requesting weather forecasts.

Start FastAPI:

```bash
uvicorn main:app --reload
```

Backend URL:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend health message |
| GET | `/api/history` | Returns the latest 14 days of historical dataset records |
| GET | `/api/predictions` | Generates and returns future solar predictions |

## Running the Frontend

Open another terminal in the Frontend directory:

```bash
npm install
npm install recharts
npm run dev
```

Open the local URL printed by Vite, usually:

http://localhost:5173

Keep the backend running while using the dashboard.

## Dashboard

The React dashboard displays summary cards, a historical and forecast output chart, and a table of future solar predictions.

Add a screenshot of the running dashboard to the repository and update the path below after saving it.

![Solar Power Dashboard](docs/solar-dashboard.png)

## Sample Prediction Output

Example structure:

| Timestamp | Predicted Solar Output |
|---|---:|
| 2026-10-19 08:00 | 413.85 |
| 2026-10-19 09:00 | 464.16 |
| 2026-10-19 10:00 | 440.56 |

Values are illustrative examples from a previous forecast run. Actual predictions change with the latest weather forecast and model.

## Design Decisions and Assumptions

- Synthetic data is used for model development because measured solar plant data is not provided.
- A chronological split is used to reduce time-series data leakage.
- Time-based features represent daily and weekly patterns.
- The IQR method is used to flag extreme numeric values during preprocessing.
- The WeatherAPI.com free forecast service is used for future weather inputs.
- Negative solar predictions are clipped to zero.
- Model evaluation metrics describe performance on synthetic validation data, not real-world measured solar output.
- The historical dataset and live forecast cover different dates.

## Limitations

- Model performance on real solar installations has not been established.
- Weather forecasts and API availability can change.
- Synthetic training data may not fully represent real weather and solar generation patterns.
- Forecast results depend on the availability and quality of weather data.

## License

This project was developed as a coding assignment.
