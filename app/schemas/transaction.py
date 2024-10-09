from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class TransactionBase(BaseModel):
  symbol: str = Field(...)
  operation: str = Field(...)
  shares: float = Field(...)
  price: float = Field(...)
  currency: str = Field(...)
  date: datetime = Field(...)
  portfolio_id: Optional[str] = Field(None)
  user_id: Optional[str] = Field(None)
  asset_id: Optional[str] = Field(None)
  fee_tax: Optional[float] = Field(None)
  notes: Optional[str] = Field(None)
  name: Optional[str] = Field(None)

  class Config:
    from_attributes = True

class TransactionResponse(TransactionBase):
  id: str
  portfolio_id: str
  user_id: Optional[str]

  class Config:
    from_attributes = True
