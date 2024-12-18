from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List, Optional


class Prediction(BaseModel):
    id: str | None = Field(default=None, alias='_id')
    symbol: str
    predicated_dates: list[str]
    predicated_prices: list[float]
    predicated_days: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.replace(tzinfo=timezone.utc).isoformat()
        }
