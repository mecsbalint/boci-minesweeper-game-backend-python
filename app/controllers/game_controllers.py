from flask import current_app, jsonify, Response, Flask, request
from flask_jwt_extended import jwt_required, current_user
from app.services.dtos import PlayerMoveDto
from app.services.game_service import create_game as create_game_service, check_active_game, get_active_game, make_player_move
from app.services.game_session_manager import GameSessionManager


def init_game_endpoints(app: Flask):

    @app.route("/api/game", methods=["POST"])
    @jwt_required()
    def create_game() -> Response:
        game_sessions: GameSessionManager = current_app.game_sessions
        game_state_dto = create_game_service(current_user, game_sessions)
        return jsonify({"gameState": game_state_dto})

    @app.route("/api/game/active", methods=["GET"])
    @jwt_required()
    def check_active_game_status():
        game_sessions = current_app.game_sessions
        active_status = check_active_game(current_user, game_sessions)

        return jsonify({"status": active_status})

    @app.route("/api/game", methods=["GET"])
    @jwt_required()
    def get_current_game() -> Response:
        game_sessions: GameSessionManager = current_app.game_sessions
        game_state_dto = get_active_game(current_user, game_sessions)
        return jsonify({"gameState": game_state_dto})

    @app.route("/api/game", methods=["PATCH"])
    @jwt_required()
    def make_move() -> Response:
        game_sessions: GameSessionManager = current_app.game_sessions
        body = request.get_json()
        player_move = PlayerMoveDto(**body)

        game_state_dto = make_player_move(current_user, game_sessions, player_move)
        return jsonify({"gameState": game_state_dto})
