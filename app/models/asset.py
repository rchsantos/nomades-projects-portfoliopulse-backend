from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

class Asset(BaseModel):
  id: Optional[str] = Field(None)
  symbol: str = Field(...)
  name: str = Field(...)
  asset_type: Optional[str] = Field(...)
  sector: Optional[str] = Field(...)
  currency: Optional[str] = Field(...)
  source: Optional[str] = Field(None)
  tags: Optional[list[str]] = Field(None)
  esg_score: Optional[int] = Field(None)
  portfolio_id: Optional[str] = Field(None)

  class Config:
    from_attributes = True
    json_encoders = { ObjectId: str }
    arbitrary_types_allowed = True

# class AssetCreate(AssetBase):
#   portfolio_id: str = Field(...)
#
#   purchase_date: datetime = Field(...)
#   purchase_price: float = Field(...),
#   quantity: float

# class Asset(AssetBase):
#   name: str = Field(...)
#   portfolio_id: str = Field(...)
#   symbol: str = Field(...)
#   purchase_date: datetime = Field(...)
#   purchase_price: float = Field(...)
#   quantity: float
#
#   class config:
#     from_attributes = True
#     json_encoders = { ObjectId: str }
