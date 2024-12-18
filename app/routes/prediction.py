import logging

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_prediction_service
from app.schemas.prediction import PredictionResponse
from app.services.prediction import PredictionService

router = APIRouter(
    prefix='/predictions',
    tags=['prediction']
)

@router.get(
    '/{symbol}/{period}',
    response_model=PredictionResponse,
    status_code=200,
    description='Get prediction for a symbol',
    response_description='Prediction retrieved successfully'
)
async def get_prediction(
    symbol: str,
    period: int = 30,
    prediction_service: PredictionService = Depends(get_prediction_service)
):
    """
    Obtain the predictions for a symbol for the next `days` days.
    :param period: Number of days to predict.
    :param prediction_service: PredictionService object.
    :param symbol: Stock symbol to predict.
    :return: PredictionResponse object.
    """
    try:
        return await prediction_service.fetch_prediction_for_symbol(symbol, period)
    except ValueError as e:
        logging.error(f'Error fetching prediction: {e}')
        raise HTTPException(status_code=400, detail=str(e))
