from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

class TransactionBase(BaseModel):
  id: Optional[str] = Field(None)
  portfolio_id: Optional[str] = Field(None)
  asset_id: Optional[str] = Field(None)
  created_at: Optional[datetime] = Field(None)
  shares: Optional[float] = Field(None)
  price_per_share: Optional[float] = Field(None)
  total_value: Optional[float] = Field(None)
  currency: Optional[str] = Field(None)
  fees: Optional[float] = Field(None)
  notes: Optional[str] = Field(None)

  class Config:
    from_attributes = True
    json_encoders = { ObjectId: str }

class TransactionCreate(TransactionBase):
  symbol: str
  transaction_type: str

class TransactionUpdate(TransactionBase):
  asset_id: Optional[str] = Field(None)
  portfolio_id: Optional[str] = Field(None)
  transaction_type: Optional[str] = Field(None)
  created_at: Optional[datetime] = Field(None)
  shares: Optional[float] = Field(None)
  price_per_share: Optional[float] = Field(None)
  total_value: Optional[float] = Field(None)
  currency: Optional[str] = Field(None)
  fees: Optional[float] = Field(None)
  notes: Optional[str] = Field(None)

  class Config:
    from_attributes = True
    json_encoders = { ObjectId: str }

class TransactionResponse(TransactionBase):
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
  notes: Optional

  class Config:
    from_attributes = True
    json_encoders = { ObjectId: str }
    arbitrary_types_allowed = True
