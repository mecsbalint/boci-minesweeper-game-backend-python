from typing import Any
import os
from dotenv import load_dotenv
from flask import Flask
from app.error_handling.error_handlers import http_exception_handler
from app.extensions import jwt
from werkzeug.exceptions import Unauthorized


def init_flask_jwt(app: Flask):
    load_dotenv()

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt.init_app(app)

    @jwt.user_lookup_loader  # pyright: ignore[reportUnknownMemberType]
    def user_lookup_callback(jwt_header: dict[str, Any], jwt_payload: dict[str, Any]) -> int:  # pyright: ignore[reportUnusedFunction]
        user_id = int(jwt_payload["sub"])
        return user_id

    @jwt.unauthorized_loader  # pyright: ignore[reportUnknownMemberType]
    def unauthorized_loader_callback(message: str):  # pyright: ignore[reportUnusedFunction]
        return http_exception_handler(Unauthorized(description=message))

    @jwt.invalid_token_loader  # pyright: ignore[reportUnknownMemberType]
    def invalid_token_loader_callback(message: str):  # pyright: ignore[reportUnusedFunction]
        return http_exception_handler(Unauthorized(description=message))

    @jwt.expired_token_loader  # pyright: ignore[reportUnknownMemberType]
    def expired_token_loader_callback(jwt_header: dict[str, Any], jwt_payload: dict[str, Any]):  # pyright: ignore[reportUnusedFunction]
        return http_exception_handler(Unauthorized(description="Token has been expired"))

    @jwt.revoked_token_loader  # pyright: ignore[reportUnknownMemberType]
    def revoked_token_loader_callback(jwt_header: dict[str, Any], jwt_payload: dict[str, Any]):  # pyright: ignore[reportUnusedFunction]
        return http_exception_handler(Unauthorized(description="Token has been revoked"))

    @jwt.needs_fresh_token_loader  # pyright: ignore[reportUnknownMemberType]
    def needs_fresh_token_loader_callback(jwt_header: dict[str, Any], jwt_payload: dict[str, Any]):  # pyright: ignore[reportUnusedFunction]
        return http_exception_handler(Unauthorized(description="Fresh token is needed"))
