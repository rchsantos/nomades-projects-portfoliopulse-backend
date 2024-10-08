from pydantic import BaseModel, Field
from typing import List, Optional

from app.models.asset import Asset


class Portfolio(BaseModel):
  id: Optional[str] = Field(None)
  user_id: str
  name: str
  assets: List[Asset] = []
  description: Optional[str] = None
  strategy: Optional[str] = None
  total_value: Optional[float] = 0.0
  total_return: Optional[float] = 0.0

  class Config:
    from_attributes = True
