from fastapi import APIRouter
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from utils.jwt_manager import create_token
from dotenv import load_dotenv

import os

user_router = APIRouter()
load_dotenv()


class User(BaseModel):
    email: str = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=5, max_length=50)


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
