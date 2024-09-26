import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
  id: Optional[str] = Field(None)
  username: str = Field(..., min_length=3, max_length=50)
  email: EmailStr
  password: str
  salt: Optional[str]
  full_name: Optional[str] = Field(None, min_length=3)
  role: Optional[str] = Field(default='user')
  is_active: Optional[bool] = Field(default=True)

  class ConfigDict:
    from_attributes = True

class UserUpdate(BaseModel):
  id: Optional[str]
  username: Optional[str] = Field(None, min_length=3, max_length=50)
  email: Optional[EmailStr]
  full_name: Optional[str] = Field(None, min_length=3)
  role: Optional[str]
  is_active: Optional[bool]
  password: Optional[str]

  class Config:
    from_attributes = True
