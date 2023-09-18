from pydantic import BaseModel, Field


class User(BaseModel):
    email_address: str = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=5, max_length=50)
