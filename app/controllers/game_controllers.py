from flask import request
from flask_jwt_extended import jwt_required, current_user
from app.services.game_service import create_game as create_game_service


def init_game_endpoints(app):

    @app.route("/api/game", methods=["POST"])
    @jwt_required()
    def create_game():
        is_successful = create_game_service(current_user)
        return is_successful
