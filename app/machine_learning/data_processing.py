import numpy as np
from sklearn.preprocessing import MinMaxScaler

def prepare_lstm_data(data: np.array, look_back: int = 60) -> tuple:
    """
    Prepare data for LSTM by creating sequences of input-output pairs.
    :param data: List of prices (e.g., closing prices).
    :param look_back: Number of historical days to consider for each prediction.
    :return: Tuple of formatted data (X, Y) and the scaler for inverse transformation.
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(np.array(data).reshape(-1, 1))

    X, Y = [], []
    for i in range(look_back, len(data_scaled)):
        X.append(data_scaled[i - look_back:i, 0]) # Take the last look_back days as input
        Y.append(data_scaled[i, 0]) # Target price to predict

    return np.array(X), np.array(Y), scaler

def calculate_mse(actual, predicted):
    """
    Calculate the mean squared error (MSE) between the actual and predicted values.
    :param actual: List of actual values
    :param predicted: List of predicted values
    :return: Mean squared error (MSE)
    """
    return np.mean((np.array(actual) - np.array(predicted)) ** 2)
