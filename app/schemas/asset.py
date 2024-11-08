from pydantic import BaseModel, Field
from typing import Optional

class AssetBase(BaseModel):
  symbol: str = Field(...)
  name: Optional[str] = None
  shares: Optional[float] = Field(None)
  purchase_price: Optional[float] = Field(None)
  currency: Optional[str] = None

class AssetUpdate(BaseModel):
  id: Optional[str] = None
  symbol: Optional[str] = None
  name: Optional[str] = None
  shares: Optional[float] = Field(None)
  purchase_price: Optional[float] = Field(None)
  currency: Optional[str] = None
  portfolio_id: Optional[str] = None
  user_id: Optional[str] = None

  class Config:
    from_attributes = True

class AssetResponse(AssetBase):
  id: Optional[str]
  portfolio_id: str
  user_id: str
  shares: Optional[float] = Field(None)
  purchase_price: Optional[float] = Field(None)

  class Config:
    from_attributes = True

class PortfolioValueResponse(BaseModel):
  total_investment: float
  total_value: float
  return_percentage: float

  class Config:
    from_attributes = True
