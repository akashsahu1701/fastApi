from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class Course(BaseModel):
    id: int
    name: str
    price: float
    is_early_bird: Optional[bool] = None


class User(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    