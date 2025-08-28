from typing import cast
from flask import current_app, jsonify, Response, request
from flask_jwt_extended import jwt_required, current_user  # pyright: ignore[reportUnknownVariableType]
from app import CustomFlask
from app.services.dtos import PlayerMoveDto
from app.services import game_service


def init_game_endpoints(app: CustomFlask):

    @app.route("/api/game", methods=["POST"])
    @jwt_required()
    def create_game() -> Response:  # pyright: ignore[reportUnusedFunction]
        game_sessions = cast(CustomFlask, current_app).game_sessions
        game_state_dto = game_service.create_game(current_user, game_sessions)
        return jsonify(game_state_dto)

    @app.route("/api/game/active", methods=["GET"])
    @jwt_required()
    def check_active_game_status():  # pyright: ignore[reportUnusedFunction]
        game_sessions = cast(CustomFlask, current_app).game_sessions
        active_status = game_service.check_active_game(current_user, game_sessions)

        return jsonify({"status": active_status})

    @app.route("/api/game", methods=["GET"])
    @jwt_required()
    def get_current_game() -> Response:  # pyright: ignore[reportUnusedFunction]
        game_sessions = cast(CustomFlask, current_app).game_sessions
        game_state_dto = game_service.get_active_game(current_user, game_sessions)
        return jsonify({"gameState": game_state_dto})

    @app.route("/api/game", methods=["PATCH"])
    @jwt_required()
    def make_move() -> Response:  # pyright: ignore[reportUnusedFunction]
        game_sessions = cast(CustomFlask, current_app).game_sessions
        body = request.get_json()
        player_move = PlayerMoveDto(**body)

        game_state_dto = game_service.make_player_move(current_user, game_sessions, player_move)
        return jsonify({"gameState": game_state_dto})
