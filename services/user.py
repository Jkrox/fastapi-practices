from fastapi import HTTPException
from config.database import session
from models.user import User as UserModel
from schemas.user import User

from typing import List


class UserService:
    def __init__(self, db: session) -> None:
        self._db: session = db

    def create_user(self, user: User) -> None:
        user_created: UserModel | None = (
            self._db.query(UserModel)
            .filter(UserModel.email_address == user.email_address)
            .first()
        )  # Verifing if the user already exists
        if user_created:
            raise HTTPException(status_code=400, detail="User already exists.")

        new_user = UserModel(
            email_address=user.email_address, password=user.password
        )

        self._db.add(new_user)
        self._db.commit()
        self._db.refresh(new_user)
        return {
            "user": new_user,
            "message": "User created successfully.",
        }

    def get_users(self) -> List[UserModel]:
        users = self._db.query(UserModel).all()
        if not users:
            raise HTTPException(status_code=404, detail="Users not found.")
        return users

    def get_user_by_id(self, id: int) -> UserModel:
        user = self._db.query(UserModel).filter(UserModel.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user

    # def authenticate_user(self, username: str, password: str) -> bool:
    #     user = (
    #         self._db.query(UserModel)
    #         .filter(UserModel.username == username)
    #         .first()
    #     )
    #     if not user:
    #         return False
    #     if not verify_password(password, user.password):
    #         return False
    #     return user
