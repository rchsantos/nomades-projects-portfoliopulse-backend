import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, constr

# Schema for login request payload
class LoginRequest(BaseModel):
  email: EmailStr
  password: str

# Schema for login response payload
class LoginResponse(BaseModel):
  access_token: str
  token_type: str

# Schema for registration request payload
class RegisterRequest(BaseModel):
  username: constr(min_length=3, max_length=50)
  email: EmailStr
  password: constr(min_length=8)
  full_name: Optional[constr(min_length=3)]

# Schema for registration response payload
class RegisterResponse(BaseModel):
  id: uuid.UUID
  username: str
  email: str
  full_name: Optional[str]
  role: str
  is_active: bool
