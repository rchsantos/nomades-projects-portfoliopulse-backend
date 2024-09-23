from dataclasses import Field
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field
)

class User(SQLModel, table=True):