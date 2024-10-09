from pydantic import BaseModel, Field
from typing import Optional

class AssetBase(BaseModel):
  symbol: str = Field(...)
  name: str = Field(...)
  shares: float = Field(...)
  purchase_price: float = Field(...),
  currency: str = Field(...)

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
  id: str
  portfolio_id: str
  user_id: str

  class Config:
    from_attributes = True
