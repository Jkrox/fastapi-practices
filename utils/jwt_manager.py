from jwt import encode, decode
from datetime import datetime, timedelta


def create_token(data: dict, secret: str) -> str:
    return encode(
        payload={**data, "exp": expire_date(minutes=2)},
        key=secret,
        algorithm="HS256",
    )


def expire_date(minutes: int) -> int:
    return datetime.utcnow() + timedelta(minutes=minutes)


def validate_token(token: str, secret: str) -> dict:
    return decode(token, key=secret, algorithms=["HS256"])
