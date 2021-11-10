"""Schema for User."""
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Base User schema."""
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    """Create input."""
    password: str = Field(..., min_length=5, max_length=16)


class UserInDB(UserBase):
    """To db."""
    hashed_password: str


class User(UserBase):
    """Output."""
    user_id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """Update input."""
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: str = Field(None, min_length=5, max_length=16)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
