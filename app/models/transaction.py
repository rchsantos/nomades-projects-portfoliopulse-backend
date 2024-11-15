from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

class Transaction(BaseModel):
  id: Optional[str] = Field(None)
  asset_id: str
  portfolio_id: str
  transaction_type: str
  created_at: datetime
  shares: float
  price_per_share: float
  total_value: float
  currency: str
  fees: Optional[float]
  notes: Optional[str]

  class Config:
    from_attributes = True
    json_encoders = { ObjectId: str }
    arbitrary_types_allowed = True
