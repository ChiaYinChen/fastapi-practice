from sqlalchemy.orm import Session

from ..models.user import User as UserModel
from ..schemas.user import UserCreate, UserInDB, UserUpdate


def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def create_user(db: Session, user: UserCreate):
    hashed_password = fake_password_hasher(user.password)
    user_in_db = UserInDB(
        **user.dict(), hashed_password=hashed_password
    )
    db_user = UserModel(**user_in_db.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_obj: UserModel, updates: UserUpdate):
    update_data = updates.dict(exclude_unset=True)
    if update_data.get("password"):
        hashed_password = fake_password_hasher(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    for key, value in update_data.items():
        setattr(db_obj, key, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)


def delete_user(db: Session, db_obj: UserModel):
    db.delete(db_obj)
    db.commit()
