from fastapi import APIRouter
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from schemas.user import User

from utils.jwt_manager import create_token
from dotenv import load_dotenv

import os

user_router = APIRouter()
load_dotenv()


@user_router.post("/login", tags=["login"])
def login(user: User):
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
def register(user: User) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Register successful",
            "token": create_token(user.dict(), os.getenv("KEY")),
        },
    )
