from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class config:
        orm_mode = True


class Course(BaseModel):
    id: int
    name: str
    price: float
    owner_id: int
    owner: User
    is_early_bird: Optional[bool] = None

    class Config:
        orm_mode = True


class CourseCreate(BaseModel):
    name: str
    price: float
    is_early_bird: Optional[bool] = None
