import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
  id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
  username: str = Field(..., min_length=3, max_length=50)
  email: EmailStr
  password: str
  salt: Optional[str]
  full_name: Optional[str] = Field(None, min_length=3)
  role: Optional[str] = Field(default='user')
  is_active: Optional[bool] = Field(default=True)

  class Config:
    from_attributes = True
