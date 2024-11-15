from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

class Asset(BaseModel):
  id: Optional[str] = Field(None)
  symbol: Optional[str] = Field(None)
  name: Optional[str] = Field(None)
  asset_type: Optional[str] = Field(None)
  sector: Optional[str] = Field(None)
  industry: Optional[str] = Field(None)
  currency: Optional[str] = Field(None)
  source: Optional[str] = Field(None)
  tags: Optional[list[str]] = Field(None)
  esg_score: Optional[int] = Field(None)
  portfolio_id: Optional[str] = Field(None)

  class Config:
    from_attributes = True
    json_encoders = { ObjectId: str }
    arbitrary_types_allowed = True
