from app.services.game_session_manager import GameSessionManager
from .user_service import get_user_by_email
from app.game.generation import generate_game


def create_game(user_email: str, game_sessions: GameSessionManager) -> bool:
    user = get_user_by_email(user_email)
    if not user:
        return False

    user_id = user.id
    game = generate_game()
    game_sessions.add_game(user_id, game)


def check_active_game(user_email: str, game_sessions: GameSessionManager) -> bool:
    user = get_user_by_email(user_email)
    user_id = user.id
    game = game_sessions.get_game(user_id)
    return True if game else False
