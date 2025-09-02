from typing import cast
from flask import current_app, jsonify, Response, request
from flask_jwt_extended import jwt_required, current_user  # pyright: ignore[reportUnknownVariableType]
from app.custom_flask import CustomFlask
from app.services.dtos import PlayerMoveDto
from app.services import game_service
from dataclasses import asdict


def init_game_endpoints(app: CustomFlask):

    @app.route("/api/game", methods=["POST"])
    @jwt_required()
    def create_game():  # pyright: ignore[reportUnusedFunction]
        game_sessions = cast(CustomFlask, current_app).game_sessions
        game_service.create_game(current_user, game_sessions)
        return Response(status=201)

    @app.route("/api/game/active", methods=["GET"])
    @jwt_required()
    def check_active_game_status():  # pyright: ignore[reportUnusedFunction]
        game_sessions = cast(CustomFlask, current_app).game_sessions
        active_status = game_service.check_active_game(current_user, game_sessions)

        return jsonify({"status": active_status}), 200

    @app.route("/api/game", methods=["GET"])
    @jwt_required()
    def get_current_game():  # pyright: ignore[reportUnusedFunction]
        game_sessions = cast(CustomFlask, current_app).game_sessions
        game_state_dto = game_service.get_active_game(current_user, game_sessions)
        return jsonify(asdict(game_state_dto)), 200

    @app.route("/api/game", methods=["PATCH"])
    @jwt_required()
    def make_move():  # pyright: ignore[reportUnusedFunction]
        game_sessions = cast(CustomFlask, current_app).game_sessions
        body = request.get_json()
        player_move = PlayerMoveDto(**body)

        game_state_dto = game_service.make_player_move(current_user, game_sessions, player_move)
        return jsonify(asdict(game_state_dto)), 200
