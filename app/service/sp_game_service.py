from typing import cast
from app.cache import handle_cache_errors
from app.error_handling.exceptions import InvalidPlayerMoveException, UserNotFoundException, GameNotFoundException
from app.game.game_factory import RectangularGameFactory
from app.game.gameplay import check_for_finish, check_for_winner, handle_player_step, populate_with_mines
from app.game.game import ActionType, Coordinates, Player
from app.service.user_service import get_user_by_id
from ..dto.game_dto import MatchDto, PlayerMoveDto
from app.extensions import cache
from app.game.match import Match, MatchState, Participant

NUM_OF_ROWS = 8
NUM_OF_COLUMNS = 8
NUM_OF_MINES = 10


@handle_cache_errors
def create_game(user_id: int):
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")

    gameFactory = RectangularGameFactory(NUM_OF_ROWS, NUM_OF_COLUMNS)
    game = gameFactory.create_game()
    game.players = {Player.PLAYER_VOID, Player.PLAYER_ONE}

    participants = {Participant(user_id=user_id, player=Player.PLAYER_ONE)}
    match = Match(game, participants=participants)

    cache.set(user_id, match)  # pyright: ignore[reportUnknownMemberType]


@handle_cache_errors
def check_active_game(user_id: int) -> bool:
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")
    return cache.has(user_id)  # pyright: ignore[reportUnknownMemberType]


@handle_cache_errors
def get_active_game(user_id: int) -> MatchDto:
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")

    match: Match | None = cache.get(user_id)  # pyright: ignore[reportUnknownMemberType]

    if not match:
        raise GameNotFoundException()
    return MatchDto.from_match(match, user_id)


@handle_cache_errors
def make_player_move(user_id: int, player_move: PlayerMoveDto) -> MatchDto:
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")

    match: Match | None = cache.get(user_id)  # pyright: ignore[reportUnknownMemberType]
    if not match:
        raise GameNotFoundException()

    game = match.game
    action_type = ActionType[player_move.action_type]
    action_coordinates = Coordinates(**player_move.coordinates)
    player = next((p.player for p in match.participants if user_id == p.user_id))

    if not game.board.get(action_coordinates):
        raise InvalidPlayerMoveException()

    if match.state == MatchState.READY:
        populate_with_mines(game.board, NUM_OF_MINES, start_cell=game.board.get(action_coordinates))
        match.state = MatchState.ACTIVE

    handle_player_step(match.game, action_type, action_coordinates, cast(Player, player))

    if check_for_finish(game):
        match.state = MatchState.FINISHED
        winning_player = check_for_winner(game)
        if winning_player:
            match.winner = next((
                participant
                for participant in match.participants
                if winning_player == participant.player
                ))
        else:
            match.winner = None
        cache.delete(user_id)  # pyright: ignore[reportUnknownMemberType]
    else:
        cache.set(user_id, match)  # pyright: ignore[reportUnknownMemberType]

    return MatchDto.from_match(match, user_id)
