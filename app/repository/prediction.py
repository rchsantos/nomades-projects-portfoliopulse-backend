from datetime import datetime, timedelta
from typing import Any, Mapping

from bson import ObjectId
from pymongo.results import InsertOneResult

from app.core.database import db
from app.models.prediction import Prediction


class PredictionRepository:
    """
    Prediction repository class to handle prediction-related operations.
    """
    def __init__(self):
        self.collection = db.get_collection('predictions')

    async def fetch_prediction(self, symbol: str, period: int) -> dict:
        """
        Fetch prediction for a symbol for the next `days` days.
        :param symbol: Stock symbol to predict.
        :param period: Number of days to predict.
        :return: PredictionResponse object.
        """
        prediction_data = await self.collection.find_one({
            'symbol': symbol,
            'predicated_days': period
        })

        return prediction_data if prediction_data else None

    async def save_prediction(self, prediction: dict) -> InsertOneResult:
        """
        Save a prediction to the database.
        :param prediction: Prediction
        :return: InsertOneResult
        """
        try:
            return await self.collection.insert_one(prediction)
        except Exception as e:
            raise ValueError(str(e))

    async def fetch_prediction_by_id(self, prediction_id: str) -> dict | None:
        """
        Fetch prediction by ID.
        :param prediction_id: Prediction ID.
        :return: PredictionResponse object.
        """
        prediction_data = await self.collection.find_one({
            '_id': ObjectId(prediction_id)
        })

        if prediction_data:
            prediction_data['_id'] = str(prediction_data['_id'])
            return prediction_data

        return None
