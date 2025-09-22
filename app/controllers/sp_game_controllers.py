from typing import Any
from flask import Flask, jsonify, Response, request
from flask_jwt_extended import jwt_required, current_user  # pyright: ignore[reportUnknownVariableType]
from app.dto.game_dto import PlayerMoveDto
from app.service import sp_game_service


def init_game_endpoints(app: Flask):

    @app.route("/api/game/sp", methods=["POST"])
    @jwt_required()
    def create_game():  # pyright: ignore[reportUnusedFunction]
        sp_game_service.create_game(current_user._get_current_object())
        return Response(status=201)

    @app.route("/api/game/sp/active", methods=["GET"])
    @jwt_required()
    def check_active_game_status():  # pyright: ignore[reportUnusedFunction]
        active_status = sp_game_service.check_active_game(current_user._get_current_object())

        return jsonify({"status": active_status}), 200

    @app.route("/api/game/sp", methods=["GET"])
    @jwt_required()
    def get_current_game():  # pyright: ignore[reportUnusedFunction]
        match_dto = sp_game_service.get_active_game(current_user._get_current_object())
        return jsonify(match_dto.model_dump(by_alias=True)), 200

    @app.route("/api/game/sp", methods=["PATCH"])
    @jwt_required()
    def make_move():  # pyright: ignore[reportUnusedFunction]
        payload: dict[Any, Any] = request.get_json()

        player_move_dto = PlayerMoveDto(**payload)

        match_dto = sp_game_service.make_player_move(current_user._get_current_object(), player_move_dto)
        return jsonify(match_dto.model_dump(by_alias=True)), 200
