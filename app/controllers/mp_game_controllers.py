from flask import Flask, Response, jsonify
from socketio import Server
from flask_jwt_extended import jwt_required, current_user  # pyright: ignore[reportUnknownVariableType]
from app.dto.game_dto import GameStatusDto
from app.service import game_service


def init_mp_game_endpoints(app: Flask, sio: Server):

    @app.route("/api/game/mp", methods=["POST"])
    @jwt_required()
    def create_game():  # pyright: ignore[reportUnusedFunction]
        game_service.create_mp_game(current_user._get_current_object(), sio)
        return Response(status=201)

    @app.route("/api/game/active", methods=["GET"])
    @jwt_required()
    def check_active_game():  # pyright: ignore[reportUnusedFunction]
        active_status = game_service.check_active_game(current_user._get_current_object(), "MP")

        status_dto = GameStatusDto(status=active_status)

        return jsonify(status_dto.model_dump(by_alias=True)), 200
