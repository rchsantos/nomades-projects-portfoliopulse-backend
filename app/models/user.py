from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, constr

class User(BaseModel):
  id: Optional[str] = Field(None)
  username: str = Field(..., min_length=3, max_length=50)
  email: EmailStr
  password: str
  salt: Optional[str]
  full_name: Optional[str] = Field(None, min_length=3)
  role: Optional[str] = Field(default='user')
  is_active: Optional[bool] = Field(default=True)

  class Config:
    from_attributes = True
    json_encoders = {ObjectId: str}

class UserUpdate(BaseModel):
  username: Optional[str] = Field(min_length=3, max_length=50)
  email: Optional[EmailStr]
  full_name: Optional[str]
  role: Optional[str]
  is_active: Optional[bool]
  password: Optional[constr(min_length=8)]

  class Config:
    from_attributes = True
    json_encoders = {ObjectId: str}

blacklist_tokens = set()
