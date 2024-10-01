from pydantic import BaseModel
from typing import List, Optional

class PortfolioBase(BaseModel):
  name: str
  description: Optional[str] = None
  tickers: Optional[List[str]] = None
  strategy: Optional[str] = None

class PortfolioResponse(BaseModel):
  id: Optional[str]
  name: str
  description: Optional[str] = None
  tickers: Optional[List[str]] = None
  strategy: Optional[str] = None
  user_id: str

  class Config:
    from_attributes = True

class PortfolioUpdate(BaseModel):
  name: Optional[str] = None
  description: Optional[str] = None
  tickers: Optional[List[str]] = None
  strategy: Optional[str] = None
