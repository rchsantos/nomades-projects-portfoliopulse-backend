import numpy as np
import tensorflow as tf
from keras.src.layers import Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

def build_lstm_model(input_shape):
    """
    Build and compile a simple LSTM model.
    :param input_shape: Shape of the input data (number of days, features).
    :return: Compiled LSTM model.
    """
    print("TensorFlow version:", tf.__version__)

    model = Sequential()
    model.add(Input(shape=input_shape))
    model.add(LSTM(units=60, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(units=120, return_sequences=False))
    model.add(Dropout(0.3))
    model.add(Dense(units=20))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    print(f"Built LSTM model with input shape {input_shape}")
    model.summary()

    return model

def predict_future_prices(model, last_sequence, scaler, period):
    """
    Predict future prices using a trained LSTM model.
    :param model: Trained LSTM model.
    :param last_sequence: Last known sequence of prices (normalized).
    :param scaler: Scaler used for normalization and inverse transformation.
    :param period: Number of days to predict.
    :return: List of predicted prices (denormalized).
    """
    predictions = []
    current_sequence = last_sequence.copy()

    for _ in range(period):
        # Reshape current sequence for prediction
        prediction = model.predict(current_sequence.reshape(1, -1, 1))
        denormalized_prediction = scaler.inverse_transform(prediction.reshape(-1, 1))[0, 0]
        predictions.append(float(denormalized_prediction))  # Convert to native float

        # Update the sequence with the new prediction
        current_sequence = np.append(current_sequence[1:], prediction)

    return predictions
