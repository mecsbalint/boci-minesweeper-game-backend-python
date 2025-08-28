from typing import Any
from flask_jwt_extended import JWTManager


def init_flask_jwt(jwt_manager: JWTManager):

    @jwt_manager.user_lookup_loader  # pyright: ignore[reportUnknownMemberType]
    def user_lookup_callback(jwt_header: dict[str, Any], jwt_payload: dict[str, Any]) -> int:  # pyright: ignore[reportUnusedFunction]
        user_id = int(jwt_payload["sub"])
        return user_id
