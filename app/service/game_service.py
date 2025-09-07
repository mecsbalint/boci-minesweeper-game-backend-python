from app.game.gameplay import handle_player_step
from app.game.models import ActionType, Coordinates, Game, GameState
from app.game.generation import generate_game
from ..dto.game_dto import GameDto, PlayerMoveDto
from app.extensions import cache


def create_game(user_id: int):
    game: Game = generate_game()
    cache.set(user_id, game)  # pyright: ignore[reportUnknownMemberType]


def check_active_game(user_id: int) -> bool:
    return cache.has(user_id)  # pyright: ignore[reportUnknownMemberType]


def get_active_game(user_id: int) -> GameDto:
    game = cache.get(user_id)  # pyright: ignore[reportUnknownMemberType]
    if not game:
        return None
    return GameDto.from_game(game)


def make_player_move(user_id: int, player_move: PlayerMoveDto) -> GameDto:
    game = cache.get(user_id)  # pyright: ignore[reportUnknownMemberType]
    action_type = ActionType[player_move.action_type]
    action_coordinates = Coordinates(**player_move.coordinates)

    if game:
        handle_player_step(game, action_type, action_coordinates)
        if game.state == GameState.FINISHED_LOST or game.state == GameState.FINISHED_WON:
            cache.delete(user_id)  # pyright: ignore[reportUnknownMemberType]
        else:
            cache.set(user_id, game)  # pyright: ignore[reportUnknownMemberType]
        return GameDto.from_game(game)
