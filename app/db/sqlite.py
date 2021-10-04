from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app/demo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # required for sqlite
)
# https://stackoverflow.com/a/63650364
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
