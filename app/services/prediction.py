from datetime import timedelta

import pandas as pd
from tensorflow.python.keras.callbacks import EarlyStopping

from app.models.prediction import Prediction
from app.repository.prediction import PredictionRepository
from app.services.portfolio import PortfolioService

from app.machine_learning.lstm import build_lstm_model, predict_future_prices
from app.machine_learning.data_processing import prepare_lstm_data

class PredictionService:
    """
    Prediction service class to handle prediction-related operations.
    """
    def __init__(self,
                 prediction_repo: PredictionRepository,
                 portfolio_service: PortfolioService
                 ) -> None:
        self.prediction_repo = prediction_repo
        self.portfolio_service = portfolio_service

    async def fetch_prediction_for_symbol(self, symbol: str, period: int) -> dict:
        """
        Fetch prediction for a symbol for the next days days.
        :param symbol: Stock symbol to predict.
        :param period: Number of days to predict.
        :return: PredictionResponse object.
        """
        # Verify if the prediction for the symbol already exists in the database
        prediction_data = await self.prediction_repo.fetch_prediction(symbol, period)
        if prediction_data:
            prediction_data['_id'] = str(prediction_data['_id'])
            prediction = Prediction(**prediction_data)
            return prediction.model_dump()

        # If the prediction does not exist, calculate the new prediction
        # @TODO: The historical data is split into start and end dates. Need to decide how to handle this.
        # Fetch the historical data for the symbol
        df: pd.DataFrame = await self.portfolio_service.fetch_historical_data(symbol)
        print('Historical data:', df.head())
        if df.empty:
            raise ValueError(f'No historical data found for symbol: {symbol}')

        # Get the close prices
        close_prices = df['Close'].values

        # Prepare the data for LSTM
        X, _, scaler = prepare_lstm_data(close_prices)

        # early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1, restore_best_weights=True, mode='auto')

        # Build and train the LSTM model
        model = build_lstm_model((X.shape[1], 1))
        model.fit(X, X, epochs=50, batch_size=16, validation_split=0.2, verbose=1)

        # Get the last sequence from the last look_back days
        last_sequence = X[-1]
        predictions = predict_future_prices(
            model=model,
            last_sequence=last_sequence,
            scaler=scaler,
            period=period
        )

        # Generate predictions for the next days days
        last_date = df['Date'].iloc[-1]
        # Check if last_date is a NaT and handle it
        if pd.isna(last_date):
            raise ValueError('The last date in the historical data is NaT (Not a Time).')

        predicated_dates = [(last_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, period + 1)]

        # Save the prediction to the database
        prediction = Prediction(
            symbol=symbol,
            predicated_dates=predicated_dates,
            predicated_prices=predictions,
            predicated_days=period,
        )

        result = await self.prediction_repo.save_prediction(prediction.model_dump())
        prediction_id = str(result.inserted_id)
        if not result.acknowledged:
            raise ValueError('Failed to save prediction to the database.')

        # Fetch the saved prediction
        saved_prediction_data = await self.prediction_repo.fetch_prediction_by_id(prediction_id)

        saved_prediction = Prediction(**saved_prediction_data)

        return {
            'symbol': saved_prediction.symbol,
            'predicated_dates': saved_prediction.predicated_dates,
            'predicated_prices': saved_prediction.predicated_prices,
            'predicated_days': saved_prediction.predicated_days,
            'created_at': saved_prediction.created_at,
            'updated_at': saved_prediction.updated_at
        }
