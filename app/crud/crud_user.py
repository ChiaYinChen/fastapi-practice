from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from ..core.security import get_password_hash
from ..crud.base import CRUDBase
from ..models.user import User as UserModel
from ..schemas.user import UserCreate, UserInDB, UserUpdate


class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):

    def get_by_id(
        self, db: Session, user_id: int
    ) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_username(
        self, db: Session, username: str
    ) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.username == username).first()  # noqa: E501

    def create(
        self, db: Session, obj_in: UserCreate
    ) -> UserModel:
        hashed_password = get_password_hash(obj_in.password)
        user_in_db = UserInDB(
            **obj_in.dict(), hashed_password=hashed_password
        )
        db_obj = UserModel(**user_in_db.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: UserModel,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)


user = CRUDUser(UserModel)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()
