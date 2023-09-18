from fastapi import APIRouter
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.user import User
from services.user import UserService
from config.database import session

from utils.jwt_manager import create_token
from dotenv import load_dotenv

import os

user_router = APIRouter()
load_dotenv()
db = session()


@user_router.post("/login", tags=["login"])
async def login(user: User):
    if user.email == "test@mail.com" and user.password == "123456":
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Login successful",
                "token": create_token(user.dict(), os.getenv("KEY")),
            },
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")


@user_router.post("/register", tags=["register"])
async def register(user: User) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Register successful",
            "token": create_token(user.dict(), os.getenv("KEY")),
        },
    )


@user_router.post("/users", tags=["Users"])
async def create_user(user: User):
    result = UserService(db).create_user(user)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": result},
    )


@user_router.get("/users", tags=["Users"])
async def get_users():
    result = UserService(db).get_users()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": jsonable_encoder(result)},
    )


@user_router.get("/users/{id}", tags=["Users"])
async def get_user(id: int):
    result = UserService(db).get_user_by_id(id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": jsonable_encoder(result)},
    )
