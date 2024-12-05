from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List

class AssetBase(BaseModel):
  name: Optional[str] = None
  sector: Optional[str] = None
  industry: Optional[str] = None
  currency: Optional[str] = None
  esg_score: Optional[int] = None
  analyst_rating: Optional[str] = None
  tags: Optional[list[str]] = None
  source: Optional[str] = None
  last_updated: Optional[str] = None
  asset_type: Optional[str] = None
  portfolio_ids: Optional[List[str]] = None

  class Config:
    from_attributes = True
    json_encoders = { ObjectId: str }

class AssetCreate(AssetBase):
  symbol: str

class AssetUpdate(BaseModel):
    id: Optional[str] = None
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
    portfolio_ids: Optional[List[str]] = None

    class Config:
        from_attributes = True
        json_encoders = { ObjectId: str }

class AssetResponse(AssetBase):
  id: Optional[str] = Field(None)
  portfolio_ids: Optional[List[str]]
  symbol: Optional[str]
  asset_type: Optional[str]
  sector: Optional[str]
  industry: Optional[str]
  currency: Optional[str]
  source: Optional[str]
  tags: Optional[list[str]]
  esg_score: Optional[int]
  analyst_rating: Optional[str] = Field(None)
  last_updated: Optional[str] = Field(None)

  class Config:
    from_attributes = True
    json_encoders = { ObjectId: str }
    arbitrary_types_allowed = True
