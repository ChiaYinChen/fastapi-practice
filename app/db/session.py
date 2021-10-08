from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False}  # required for sqlite
)
# https://stackoverflow.com/a/63650364
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
