from jwt import encode

def create_token(data: dict, secret: str) -> str:
    return encode(payload=data, key=secret, algorithm="HS256")