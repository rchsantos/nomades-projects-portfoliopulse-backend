import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluate_predictions(y_true, y_pred):
    """
    Evaluate the predictions with common metrics: RMSE, MAE, R².

    :param y_true: Actual values.
    :param y_pred: Predicted values.
    :return: Dictionary with RMSE, MAE, and R² scores.
    """
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    return {"RMSE": rmse, "MAE": mae, "R2": r2}
