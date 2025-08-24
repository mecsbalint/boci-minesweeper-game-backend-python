from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.services.user_service import create_user, validate_user


def init_user_endpoints(app):

    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user_name = validate_user(email, password)

        if not user_name:
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=email)
        return jsonify({"jwt": access_token, "name": user_name})

    @app.route("/api/registration", methods=["POST"])
    def registration():
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        is_succesful = create_user(name, email, password)
        status_code = 201 if is_succesful else 409

        return jsonify({"is_succesful": is_succesful}), status_code
