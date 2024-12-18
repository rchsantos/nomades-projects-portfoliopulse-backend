from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class PredictionResponse(BaseModel):
    symbol: str
    predicated_dates: List[str]
    predicated_prices: List[float]
    predicated_days: int
    created_at: datetime
    updated_at: datetime
