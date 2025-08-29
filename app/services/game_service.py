from app.game.gameplay import handle_player_step
from app.game.models import ActionType, Coordinates, Game
from app.services.game_session_manager import GameSessionManager
from app.game.generation import generate_game
from .dtos import GameDto, PlayerMoveDto


def create_game(user_id: int, game_sessions: GameSessionManager) -> GameDto | None:
    game: Game = generate_game()
    game_sessions.add_game(user_id, game)

    return GameDto.from_game(game)


def check_active_game(user_id: int, game_sessions: GameSessionManager) -> bool:
    game = game_sessions.get_game(user_id)
    return True if game else False


def get_active_game(user_id: int, game_sessions: GameSessionManager) -> GameDto | None:
    game = game_sessions.get_game(user_id)
    if not game:
        return None
    return GameDto.from_game(game)


def make_player_move(user_id: int, game_sessions: GameSessionManager, player_move: PlayerMoveDto) -> GameDto | None:
    game = game_sessions.get_game(user_id)
    action_type = ActionType[player_move.action_type]
    action_coordinates = Coordinates(**player_move.coordinates)

    if game:
        handle_player_step(game, action_type, action_coordinates)
        return GameDto.from_game(game)
    return None
