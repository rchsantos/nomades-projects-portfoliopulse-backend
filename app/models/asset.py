from typing import Optional

from pydantic import BaseModel, Field

class Asset(BaseModel):
  id: Optional[str] = Field(None)
  portfolio_id: str = Field(...)
  symbol: str = Field(...)
  name: str = Field(...)
  shares: float = Field(...)
  purchase_price: float = Field(...),
  currency: str = Field(...)
  user_id: Optional[str] = Field(None)

  class Config:
    from_attributes = True
