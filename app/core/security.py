from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from ..core.config import settings


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    #  (Expiration Time) Token 的過期時間
    payload["exp"] = expire

    # (Issued At) Token 的發行時間
    payload["iat"] = datetime.utcnow()

    # (Subject) 使用該 Token 的使用者
    payload["sub"] = str(sub)
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  # noqa: E501
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)
