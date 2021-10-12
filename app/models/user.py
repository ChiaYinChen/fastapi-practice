from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from ..db.base_class import Base


class User(Base):
    """Table for user."""

    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(256), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(64), nullable=True)
    created_time = Column(DateTime, nullable=False, default=datetime.now)
    is_active = Column(Boolean, server_default=expression.true(), default=True)
