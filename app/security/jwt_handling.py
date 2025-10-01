from jwt import decode  # pyright: ignore[reportUnknownVariableType]
from app.security import JWT_SECRET_KEY  # pyright: ignore[reportUnknownVariableType]


def decode_jwt_token(token: str) -> int:
    jwt_payload = decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    user_id = int(jwt_payload["sub"])
    return user_id
