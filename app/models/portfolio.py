from pydantic import BaseModel, Field
from typing import List, Optional

class Portfolio(BaseModel):
  id: Optional[str] = Field(None)
  name: str
  description: Optional[str] = None
  tickers: Optional[List[str]] = None
  user_id: str
  strategy: Optional[str] = None
