from app.game.gameplay import handle_player_step
from app.game.models import ActionType, Coordinates, Game
from app.services.game_session_manager import GameSessionManager
from .user_service import get_user_by_email
from app.game.generation import generate_game
from .dtos import GameDto, PlayerMoveDto


def create_game(user_email: str, game_sessions: GameSessionManager) -> GameDto | None:
    user = get_user_by_email(user_email)
    if not user:
        return None

    user_id = user.id
    game: Game = generate_game()
    game_sessions.add_game(user_id, game)

    return GameDto(game)


def check_active_game(user_email: str, game_sessions: GameSessionManager) -> bool:
    user = get_user_by_email(user_email)
    user_id = user.id
    game = game_sessions.get_game(user_id)
    return True if game else False


def get_active_game(user_email: str, game_sessions: GameSessionManager) -> GameDto:
    user = get_user_by_email(user_email)
    user_id = user.id
    game = game_sessions.get_game(user_id)
    if not game:
        return None
    return GameDto(game)


def make_player_move(user_email: str, game_sessions: GameSessionManager, player_move: PlayerMoveDto) -> GameDto:
    user = get_user_by_email(user_email)
    user_id = user.id
    game = game_sessions.get_game(user_id)
    action_type = ActionType[player_move.action_type]
    action_coordinates = Coordinates(**player_move.coordinates)

    handle_player_step(game, action_type, action_coordinates)

    return GameDto(game)
