from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional

class UserBase(BaseModel):
  full_name: Optional[str] = Field(None, min_length=3)
  role: Optional[str] = Field(default='user')
  is_active: Optional[bool] = Field(default=True)

class UserCreate(UserBase):
  username: str = Field(..., min_length=3, max_length=50)
  email: EmailStr
  password: constr(min_length=8)

class UserResponse(UserBase):
  id: Optional[str]
  username: Optional[str]
  email: Optional[EmailStr]

  class Config:
    from_attributes = True
    json_encoders = {ObjectId: str}

class UserResponseVerify(UserBase):
  username: str
  salt: str
  password: str

  class Config:
    from_attributes = True
    json_encoders = {ObjectId: str}

class UserUpdate(UserBase):
  username: Optional[str] = Field(None, min_length=3, max_length=50)
  email: Optional[EmailStr] = Field(None)
  password: Optional[constr(min_length=8)] = Field(None)

class UserAuthResponse(UserBase):
  access_token: str
  token_type: str

  class Config:
    from_attributes = True
