from flask import request, jsonify, Flask
from flask_jwt_extended import create_access_token  # pyright: ignore[reportUnknownVariableType]
from app.services.dtos import JwtResponseDto
from app.services.user_service import create_user, validate_user


def init_user_endpoints(app: Flask):

    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        validation_response = validate_user(email, password)

        if not validation_response:
            return jsonify({"msg": "Bad username or password"}), 401

        user_id, user_name = validation_response

        access_token = create_access_token(identity=user_id)
        response_obj = JwtResponseDto(access_token, user_name)
        return jsonify(response_obj)

    @app.route("/api/registration", methods=["POST"])
    def registration():
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        is_succesful = create_user(name, email, password)
        status_code = 201 if is_succesful else 409

        return jsonify({"is_succesful": is_succesful}), status_code
