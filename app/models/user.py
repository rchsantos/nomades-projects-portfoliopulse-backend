from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = True


class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
