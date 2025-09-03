from typing import Any
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from app.custom_flask import CustomFlask


def init_flask_jwt(app: CustomFlask, jwt_manager: JWTManager):
    load_dotenv()

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt_manager.init_app(app)

    @jwt_manager.user_lookup_loader  # pyright: ignore[reportUnknownMemberType]
    def user_lookup_callback(jwt_header: dict[str, Any], jwt_payload: dict[str, Any]) -> int:  # pyright: ignore[reportUnusedFunction]
        user_id = int(jwt_payload["sub"])
        return user_id
