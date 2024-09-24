from typing import Optional
from pydantic import BaseModel, UUID4

class User(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]


class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool

    class Config:
        orm_mode = True
