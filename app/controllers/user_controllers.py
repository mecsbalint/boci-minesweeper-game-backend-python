import datetime
from flask import Flask, abort, request, jsonify
from flask_jwt_extended import create_access_token  # pyright: ignore[reportUnknownVariableType]
from app.dto.dtos import JwtResponseDto
from app.service import user_service
from dataclasses import asdict


def init_user_endpoints(app: Flask):

    @app.route("/api/login", methods=["POST"])
    def login():  # pyright: ignore[reportUnusedFunction]
        data: dict[str, str] | None = request.get_json()

        if not isinstance(data, dict):
            abort(400, description="Invalid request body")

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            abort(400, description="Email and password are required")

        user = user_service.validate_user(email, password)

        expires = datetime.timedelta(hours=1)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        response_obj = JwtResponseDto(access_token, user.name)
        return jsonify(asdict(response_obj))

    @app.route("/api/registration", methods=["POST"])
    def registration():  # pyright: ignore[reportUnusedFunction]
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        is_successful = user_service.create_user(name, email, password)
        status_code = 201 if is_successful else 409

        return jsonify({"is_successful": is_successful}), status_code
