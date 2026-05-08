import os
import numpy as np
import pandas as pd
import pickle
from django.conf import settings

# -------------------------------
# PATHS
# -------------------------------
MODEL_PATH = os.path.join(settings.BASE_DIR, 'predictor', 'model', 'model.h5')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'predictor', 'model', 'scaler.pkl')


# -------------------------------
# REBUILD MODEL FROM SCRATCH + LOAD WEIGHTS
# -------------------------------
def load_model_patched(model_path):
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(60, 1)),
        LSTM(50, return_sequences=False),
        Dense(1)
    ])

    model.load_weights(model_path)
    return model

model = load_model_patched(MODEL_PATH)

# LOAD SCALER
# -------------------------------
with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)

# GET LATEST UPLOADED FILE
# -------------------------------
def get_latest_file(request):
    filename = request.session.get('latest_file')
    if not filename:
        return None
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if not os.path.exists(file_path):
        return None
    return file_path

# PREDICTION FUNCTION
# -------------------------------
def predict_prices(request, days=1):
    file_path = get_latest_file(request)
    if not file_path:
        return None

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()

    if 'close_price' not in df.columns:
        return None

    data = df[['close_price']].values
    scaled_data = scaler.transform(data)

    time_step = 60
    if len(scaled_data) < time_step:
        return None

    last_60 = scaled_data[-time_step:]
    current_input = last_60.reshape(1, time_step, 1)

    predictions = []
    for _ in range(days):
        pred = model.predict(current_input, verbose=0)
        predictions.append(pred[0][0])

        # Fixed sliding window
        new_val = np.array([[[pred[0][0]]]])
        current_input = np.append(current_input[:, 1:, :], new_val, axis=1)

    # Convert predictions back to original scale
    predictions = scaler.inverse_transform(
        np.array(predictions).reshape(-1, 1)
    ).flatten().tolist()

    #  Last 60 actual prices for the chart
    historical = scaler.inverse_transform(
        last_60.reshape(-1, 1)
    ).flatten().tolist()

    return {
        'predictions': predictions,
        'historical': historical,
    }


