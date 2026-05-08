# Stock Price Prediction System

An AI-powered web application to predict future stock closing prices using LSTM (Long Short-Term Memory) neural networks built with Django.

## About

This project uses deep learning to forecast NSE stock prices based on 5 years of historical market data. Users can upload their stock CSV data and generate predictions for the next 1 day, 7 days, or 30 days with interactive price charts.

## Files

- `predictor/predictor.py` — LSTM model loading and prediction logic
- `predictor/views.py` — Django views for prediction, charts, and dashboard
- `predictor/urls.py` — URL routing for the predictor app
- `accounts/views.py` — User authentication (register, login, logout)
- `templates/predictor/` — HTML templates for dashboard, predict, charts, info pages
- `static/css/dashboard.css` — Main stylesheet for the entire application
- `predictor/model/model.h5` — Trained LSTM model weights
- `predictor/model/scaler.pkl` — MinMaxScaler for data preprocessing

## Features

- User Registration and Login with credentials stored in SQLite database
- CSV Upload with automatic data cleaning pipeline
- LSTM-based stock price prediction (1-day, 7-day, 30-day)
- Interactive Chart.js visualization — historical vs predicted prices
- Live NSE stock charts with 10-day moving average using yFinance
- Model Info & Help page explaining the architecture and usage

## Getting Started

1. Clone the repository
2. Create and activate a virtual environment
```bash
python3 -m venv env
source env/bin/activate
```
3. Install dependencies
```bash
pip install django tensorflow==2.6.0 numpy==1.21.6 pandas scikit-learn yfinance h5py
```
4. Run migrations
```bash
python3 manage.py migrate
```
5. Start the server
```bash
python3 manage.py runserver
```

## Usage

1. Visit `http://127.0.0.1:8000/register/` and create an account
2. Login with your credentials
3. Go to **Data Cleaning** and upload a CSV file with a `close_price` column (minimum 60 rows)
4. Go to **Predict Price**, select forecast range and click Generate Forecast
5. View the historical vs predicted price chart
6. Go to **View Charts** and enter any NSE symbol (e.g. TCS.NS) for live data

## Model Architecture

| Layer | Details |
|-------|---------|
| Input | 60 timesteps × 1 feature (close price) |
| LSTM 1 | 50 units, return_sequences=True |
| LSTM 2 | 50 units |
| Dense | 1 unit (predicted price) |
| Scaler | MinMaxScaler (0 to 1) |

## Tech Stack

- **Backend:** Python, Django, TensorFlow/Keras
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Data:** Pandas, NumPy, Scikit-learn, yFinance
- **Database:** SQLite
- **Model:** LSTM Neural Network

## Contact

For any inquiries feel free to contact via email at `your_email@gmail.com`

## Results

<!-- Add your screenshots here after uploading them to GitHub -->
<!-- ![Login Page](screenshots/login.png) -->
<!-- ![Predict Page](screenshots/predict.png) -->
<!-- ![Chart Page](screenshots/chart.png) -->
