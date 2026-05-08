from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
# import yfinance as yf
from django.http import JsonResponse
from django.shortcuts import render
from .predictor import predict_prices

@login_required
def dashboard(request):
    return render(request, 'predictor/dashboard.html')

@login_required
def upload_dataset(request):
    context = {}

    if request.method == "POST":
        file = request.FILES['file']
        df = pd.read_csv(file)

        context['data'] = df.head(10).values.tolist()
        context['columns'] = df.columns.tolist()

    return render(request, 'predictor/upload.html', context)

model = None

# def get_model():
#     global model

#     if model is None:
#         from tensorflow.keras.models import Sequential
#         from tensorflow.keras.layers import LSTM, Dense

#         model = Sequential()
#         model.add(LSTM(50, return_sequences=True, input_shape=(60, 1)))
#         model.add(LSTM(50))
#         model.add(Dense(1))

#         model.load_weights("/YOUR_PATH/lstm_model_new.h5")

#     return model

# @login_required
def predict_view(request):
    result = None
    days = 1
    historical = []
    predictions = []

    if request.method == 'POST':
        days = int(request.POST.get('days'))
        raw = predict_prices(request, days)

        if raw:
            historical = raw['historical']
            predictions = raw['predictions']

            if days == 30:
                result = {
                    'min_price': min(predictions),
                    'max_price': max(predictions),
                    'trend': 'up' if predictions[-1] > predictions[0] else 'down'
                }
            else:
                result = predictions

    return render(request, 'predictor/predict.html', {
        'result': result,
        'days': days,
        'historical': historical,
        'predictions': predictions,
    })



# def predict_view(request):

#     result = None
#     days = 1

#     if request.method == 'POST':
#         days = int(request.POST.get('days'))
#         result = predict_prices(request, days)

#     return render(request, 'predictor/predict.html', {
#         'result': result,
#         'days': days
#     })
    
@login_required
def predict_page(request):
    return render(request, 'predictor/predict.html')

def chart_data(request):
    import yfinance as yf

    stock = request.GET.get('stock', 'TCS.NS')

    data = yf.download(stock, period="6mo", auto_adjust=True)

    close = data['Close'].squeeze()  #  ensures it's a Series not DataFrame
    ma = close.rolling(10).mean()

    return JsonResponse({
        "dates": data.index.strftime('%Y-%m-%d').tolist(),
        "prices": close.tolist(),
        "ma": ma.fillna(0).tolist()
    })

@login_required
def charts_page(request):
    return render(request, 'predictor/charts.html')

# @login_required
def info_page(request):
    return render(request, 'predictor/info.html')