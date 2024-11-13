from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List

class AssetBase(BaseModel):
  name: Optional[str] = None
  sector: Optional[str] = None
  currency: Optional[str] = None
  esg_score: Optional[int] = None
  analyst_rating: Optional[str] = None
  tags: Optional[list[str]] = None
  source: Optional[str] = None
  last_updated: Optional[str] = None
  portfolio_id: Optional[str] = None

  class Config:
    from_attributes = True
    json_encoders = { ObjectId: str }

class AssetCreate(AssetBase):
  symbol: str = Field(...)
  asset_type: str = Field(...)

class AssetUpdate(BaseModel):
  symbol: Optional[str] = None
  name: Optional[str] = None
  asset_type: Optional[str] = None
  sector: Optional[str] = None
  currency: Optional[str] = None
  esg_score: Optional[int] = None
  analyst_rating: Optional[str] = None
  tags: Optional[List[str]] = None
  source: Optional[str] = None
  last_updated: Optional[str] = None
  portfolio_id: Optional[str] = None

  class Config:
    from_attributes = True
    json_encoders = { ObjectId: str }

class AssetResponse(AssetBase):
  id: Optional[str] = Field(None, alias='_id')
  portfolio_id: str
  symbol: str
  asset_type: str

  class Config:
    from_attributes = True
    json_encoders = { ObjectId: str }
    arbitrary_types_allowed = True
