from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):

    username: str
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):

    password: str = Field(..., min_length=5, max_length=16)


class UserInDB(UserBase):

    hashed_password: str


class User(UserBase):

    user_id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):

    email: Optional[str] = None
    full_name: Optional[str] = None
    password: str = Field(None, min_length=5, max_length=16)
    is_active: bool = None
