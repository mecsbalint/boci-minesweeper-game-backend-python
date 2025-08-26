from flask import current_app
from flask_jwt_extended import jwt_required, current_user
from app.services.game_service import create_game as create_game_service


def init_game_endpoints(app):

    @app.route("/api/game", methods=["POST"])
    @jwt_required()
    def create_game():
        game_sessions = current_app.game_sessions
        is_successful = create_game_service(current_user, game_sessions)
        return is_successful
