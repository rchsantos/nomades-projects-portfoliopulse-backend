import uuid
from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional

# Schema base for User with common fields
class UserBase(BaseModel):
  username: str = Field(..., min_length=3, max_length=50)
  email: EmailStr
  full_name: Optional[str] = Field(None, min_length=3)
  role: Optional[str] = Field(default='user')
  is_active: Optional[bool] = Field(default=True)

# Schema for User creation
class UserCreate(UserBase):
  password: constr(min_length=8)

# Schema for the User response
class UserResponse(UserBase):
  id: uuid.UUID

  class Config:
    from_attributes = True

# Schema for User update
class UserUpdate(UserBase):
  username: Optional[str] = Field(None, min_length=3, max_length=50)
  email: Optional[EmailStr]
  full_name: Optional[str] = Field(None, min_length=3)
  role: Optional[str]
  is_active: Optional[bool]
  password: Optional[constr(min_length=8)]

# Schema for the Auth response
class UserAuthResponse(UserBase):
  access_token: str
  token_type: str

  class Config:
    from_attributes = True
