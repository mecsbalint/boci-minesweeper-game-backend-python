from app.cache import handle_cache_errors
from app.error_handling.exceptions import UserNotFoundException, GameNotFoundException
from app.game.gameplay import handle_player_step
from app.game.models import ActionType, Coordinates, Game, GameState
from app.game.generation import __generate_base_game_board
from app.service.user_service import get_user_by_id
from ..dto.game_dto import GameDto, PlayerMoveDto
from app.extensions import cache

NUM_OF_ROWS = 8
NUM_OF_COLUMNS = 8


@handle_cache_errors
def create_game(user_id: int):
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")
    game: Game = __generate_base_game_board(NUM_OF_ROWS, NUM_OF_COLUMNS)
    cache.set(user_id, game)  # pyright: ignore[reportUnknownMemberType]


@handle_cache_errors
def check_active_game(user_id: int) -> bool:
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")
    return cache.has(user_id)  # pyright: ignore[reportUnknownMemberType]


@handle_cache_errors
def get_active_game(user_id: int) -> GameDto:
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")
    game: Game | None = cache.get(user_id)  # pyright: ignore[reportUnknownMemberType]
    if not game:
        raise GameNotFoundException()
    return GameDto.from_game(game)


@handle_cache_errors
def make_player_move(user_id: int, player_move: PlayerMoveDto) -> GameDto:
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")

    game: Game | None = cache.get(user_id)  # pyright: ignore[reportUnknownMemberType]
    if not game:
        raise GameNotFoundException()

    action_type = ActionType[player_move.action_type]
    action_coordinates = Coordinates(**player_move.coordinates)

    handle_player_step(game, action_type, action_coordinates)

    if game.state == GameState.FINISHED_LOST or game.state == GameState.FINISHED_WON:
        cache.delete(user_id)  # pyright: ignore[reportUnknownMemberType]
    else:
        cache.set(user_id, game)  # pyright: ignore[reportUnknownMemberType]
    return GameDto.from_game(game)
