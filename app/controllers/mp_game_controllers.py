from flask import Flask, Response
from flask_jwt_extended import jwt_required, current_user  # pyright: ignore[reportUnknownVariableType]
from app.service import mp_game_service


def init_mp_game_endpoints(app: Flask):

    @app.route("/api/game/mp", methods=["POST"])
    @jwt_required()
    def create_game():  # pyright: ignore[reportUnusedFunction]
        mp_game_service.create_game(current_user._get_current_object())
        return Response(status=201)
