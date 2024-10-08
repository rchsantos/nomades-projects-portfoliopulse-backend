from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    id: Optional[str] = Field(None)
    portfolio_id: str = Field(...)
    symbol: str = Field(...)
    operation: str = Field(...) # "buy" ou "sell"
    shares: float = Field(...)
    price: float = Field(...)
    currency: str = Field(...)
    date: datetime = Field(...)
    asset_id: Optional[str] = Field(None)
    fee_tax: Optional[float] = Field(None)
    notes: Optional[str] = Field(None)
    user_id: Optional[str] = Field(None)

    class Config:
      from_attributes = True
