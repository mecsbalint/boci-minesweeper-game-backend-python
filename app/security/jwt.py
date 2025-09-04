from typing import Any
import os
from dotenv import load_dotenv
from flask import Flask
from app.extensions import jwt


def init_flask_jwt(app: Flask):
    load_dotenv()

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt.init_app(app)

    @jwt.user_lookup_loader  # pyright: ignore[reportUnknownMemberType]
    def user_lookup_callback(jwt_header: dict[str, Any], jwt_payload: dict[str, Any]) -> int:  # pyright: ignore[reportUnusedFunction]
        user_id = int(jwt_payload["sub"])
        return user_id
