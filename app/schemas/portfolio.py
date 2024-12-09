from bson import ObjectId
from pydantic import BaseModel
from typing import List, Optional

from app.models.asset import Asset


class PortfolioBase(BaseModel):
    description: Optional[str] = None
    assets: Optional[List] = None
    strategy: Optional[str] = None
    currency: Optional[str] = None


class PortfolioCreate(PortfolioBase):
    name: str
    user_id: Optional[str] = None


class PortfolioResponse(PortfolioBase):
    name: str
    id: Optional[str]
    user_id: Optional[str] = None

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}


class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    assets: Optional[List[Asset]] = None
    strategy: Optional[str] = None,
    currency: Optional[str] = None


class PortfolioHoldingsResponse(BaseModel):
    holdings: List[Asset]


class WeightDetail(BaseModel):
    asset: Asset
    quantity: float
    current_value: float
    weight: float


class PortfolioAnalysisResponse(BaseModel):
    total_value: float
    weights: List[WeightDetail]
