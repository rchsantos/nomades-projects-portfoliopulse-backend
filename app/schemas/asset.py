from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AssetBase(BaseModel):
  name: str = Field(...)
  symbol: str = Field(...)
  quantity: float = Field(...)
  purchase_price: float = Field(...)
  currency: str = Field(...)
  portfolio_id: str = Field(None)

class AssetCreate(AssetBase):
  user_id: Optional[str] = Field(None)

  class Config:
    from_attributes = True

class AssetResponse(AssetBase):
  id: str
  user_id: str

  class Config:
    from_attributes = True
