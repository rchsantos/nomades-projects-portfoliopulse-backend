from typing import Optional

from pydantic import BaseModel, Field

class Asset(BaseModel):
  id: Optional[str] = Field(None)
  name: str = Field(...)
  symbol: str = Field(...)
  quantity: float = Field(...)
  purchase_price: float = Field(...),
  currency: str = Field(...)
  portfolio_id: str = Field(None)
  user_id: Optional[str] = Field(None)

  class Config:
    from_attributes = True
