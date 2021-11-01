"""Schema for Token."""
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Output."""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Token payload."""
    sub: Optional[str] = None
