import uuid
from typing import Optional
from pydantic import BaseModel

# Schema for login request payload
class LoginRequest(BaseModel):
  username: str
  password: str

# Schema for login response payload
class LoginResponse(BaseModel):
  access_token: str
  token_type: str

# Schema for registration response payload
class RegisterResponse(BaseModel):
  id: str
  username: str
  email: str
  full_name: Optional[str]
  role: str
  is_active: bool
