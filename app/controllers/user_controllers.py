from flask import request, jsonify
from flask_jwt_extended import create_access_token  # pyright: ignore[reportUnknownVariableType]
from app.custom_flask import CustomFlask
from app.services.dtos import JwtResponseDto
from app.services import user_service
from dataclasses import asdict


def init_user_endpoints(app: CustomFlask):

    @app.route("/api/login", methods=["POST"])
    def login():  # pyright: ignore[reportUnusedFunction]
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        validation_response = user_service.validate_user(email, password)

        if not validation_response:
            return jsonify({"msg": "Bad username or password"}), 401

        user_id, user_name = validation_response

        access_token = create_access_token(identity=user_id)
        response_obj = JwtResponseDto(access_token, user_name)
        return jsonify(asdict(response_obj))

    @app.route("/api/registration", methods=["POST"])
    def registration():  # pyright: ignore[reportUnusedFunction]
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        is_succesful = user_service.create_user(name, email, password)
        status_code = 201 if is_succesful else 409

        return jsonify({"is_succesful": is_succesful}), status_code
