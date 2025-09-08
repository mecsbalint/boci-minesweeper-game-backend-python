import datetime
from flask import Flask, request, jsonify, Response
from flask_jwt_extended import create_access_token  # pyright: ignore[reportUnknownVariableType]
from app.service import user_service
from dataclasses import asdict
from app.dto.user_dto import JwtResponseDto, UserLoginDto, UserRegistrationDto
from typing import Any


def init_user_endpoints(app: Flask):

    @app.route("/api/login", methods=["POST"])
    def login():  # pyright: ignore[reportUnusedFunction]
        payload: dict[Any, Any] = request.get_json()

        user_login_dto = UserLoginDto(**payload)
        email = user_login_dto.email
        password = user_login_dto.password

        user = user_service.validate_user(email, password)

        expires = datetime.timedelta(hours=1)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        response_obj = JwtResponseDto(jwt=access_token, name=user.name)
        return jsonify(asdict(response_obj))

    @app.route("/api/registration", methods=["POST"])
    def registration():  # pyright: ignore[reportUnusedFunction]
        payload: dict[Any, Any] = request.get_json()

        user_registration_dto = UserRegistrationDto(**payload)

        name = user_registration_dto.name
        email = user_registration_dto.email
        password = user_registration_dto.password

        user_service.create_user(name, email, password)

        return Response(status=201)
