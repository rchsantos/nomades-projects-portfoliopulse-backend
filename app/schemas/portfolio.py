from pydantic import BaseModel
from typing import List, Optional

from app.schemas.asset import AssetResponse

class PortfolioBase(BaseModel):
  name: str
  description: Optional[str] = None
  assets: Optional[List[AssetResponse]] = None
  strategy: Optional[str] = None

class PortfolioResponse(BaseModel):
  id: Optional[str]
  name: str
  description: Optional[str] = None
  assets: Optional[List[AssetResponse]] = None
  strategy: Optional[str] = None
  user_id: str
  currency: Optional[str] = None

  class Config:
    from_attributes = True

class PortfolioUpdate(BaseModel):
  name: Optional[str] = None
  description: Optional[str] = None
  assets: Optional[List[str]] = None
  strategy: Optional[str] = None
