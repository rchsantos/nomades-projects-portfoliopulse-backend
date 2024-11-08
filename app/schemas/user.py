from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional

class UserBase(BaseModel):
  """ Schema base for User with common fields """
  full_name: Optional[str] = Field(None, min_length=3)
  role: Optional[str] = Field(default='user')
  is_active: Optional[bool] = Field(default=True)

class UserCreate(UserBase):
  """ Schema for User creation """
  username: str = Field(..., min_length=3, max_length=50)
  email: EmailStr
  password: constr(min_length=8)

class UserResponse(UserBase):
  """ Schema for User response """
  id: Optional[str]
  username: Optional[str]
  email: Optional[EmailStr]

  class Config:
    from_attributes = True
    json_encoders = {ObjectId: str}

class UserResponseVerify(UserBase):
  """ Schema for User response """
  username: str
  salt: str
  password: str

  class Config:
    from_attributes = True
    json_encoders = {ObjectId: str}

class UserUpdate(UserBase):
  """ Schema for User update """
  username: Optional[str] = Field(None, min_length=3, max_length=50)
  email: Optional[EmailStr] = Field(None)
  password: Optional[constr(min_length=8)] = Field(None)

class UserAuthResponse(UserBase):
  """ Schema for User authentication response """
  access_token: str
  token_type: str

  class Config:
    from_attributes = True
