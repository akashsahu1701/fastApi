from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class Course(BaseModel):
    id: int
    name: str
    price: float
    is_early_bird: Optional[bool] = None


class User(BaseModel):
    id: int
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class config:
        orm_mode = True
