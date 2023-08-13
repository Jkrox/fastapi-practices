import os
from dotenv import load_dotenv

from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request
from fastapi.security.http import HTTPAuthorizationCredentials
from utils.jwt_manager import validate_token

load_dotenv()

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        auth: HTTPAuthorizationCredentials | None = await super().__call__(request)
        data = validate_token(auth.credentials, os.getenv("KEY"))
        if data["email"] == None and data["email"] != "test@gmail.com":
            raise HTTPException(status_code=403, detail="Invalid crendentials")
