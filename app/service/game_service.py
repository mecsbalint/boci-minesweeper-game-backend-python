from uuid import UUID
from app.error_handling.exceptions import (GameIsFullException,
                                           InvalidBoardException, InvalidGameStateException,
                                           InvalidPlayerMoveException,
                                           UserNotFoundException,
                                           GameNotFoundException)
from app.game.game_factory import RectangularGameFactory
from app.game.gameplay import (check_for_finish,
                               check_for_winner,
                               get_cell_block,
                               handle_player_step,
                               populate_with_mines,
                               remove_mines)
from app.game.game import ActionType, Coordinates, Player
from app.service.user_service import get_user_by_id
from ..dto.game_dto import MatchDto, PlayerMoveDto
from app.game.match import Match, MatchState, Participant
from app.cache.match_cache import (SaveType,
                                   get_match_by_id_from_cache,
                                   save_match_to_cache,
                                   get_match_by_user_id_from_cache,
                                   remove_match_from_cache,
                                   check_match_in_cache,
                                   add_match_to_user_in_cache)


def create_sp_game(user_id: int):
    num_of_rows = 8
    num_of_columns = 8

    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")

    gameFactory = RectangularGameFactory(num_of_rows, num_of_columns)
    game = gameFactory.create_game()
    game.players = {Player.PLAYER_VOID, Player.PLAYER_ONE}

    participants = {Participant(user_id=user_id, player=Player.PLAYER_ONE)}
    match = Match(game, participants=participants)
    match.state = MatchState.READY

    save_match_to_cache(match, "SP")  # pyright: ignore[reportUnknownMemberType]


def create_mp_game(user_id: int):
    num_of_rows = 15
    num_of_columns = 15
    num_of_mines = 12
    num_of_players = 2
    start_positions = [Coordinates(3, 8), Coordinates(12, 8)]

    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")

    gameFactory = RectangularGameFactory(num_of_rows, num_of_columns)
    game = gameFactory.create_game()

    for _ in range(10):

        populate_with_mines(game.board, num_of_mines, action_coordinates=start_positions)

        if game.board.get(start_positions[1]) in get_cell_block(game, start_positions[0]):
            remove_mines(game.board)
            continue

        game.players = {*list(Player)[:num_of_players]}
        participants = {Participant(user_id=user_id, player=Player.PLAYER_ONE)}
        match = Match(game, participants=participants)
        match.state = MatchState.WAITING
        save_match_to_cache(match, "MP")
        return None

    raise InvalidBoardException()


def check_active_game(user_id: int, game_type: SaveType) -> bool:
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")
    return check_match_in_cache(user_id, game_type)  # pyright: ignore[reportUnknownMemberType]


def get_active_game(user_id: int, game_type: SaveType) -> MatchDto:
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")

    match: Match | None = get_match_by_user_id_from_cache(user_id, game_type)  # pyright: ignore[reportUnknownMemberType]

    if not match:
        raise GameNotFoundException()

    return MatchDto.from_match(match, user_id)


def add_user_to_match(user_id: int, match_id: UUID, game_type: SaveType) -> MatchDto:
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")

    match = get_match_by_id_from_cache(match_id, game_type)

    free_player_slots = {player for player in match.game.players if player is not Player.PLAYER_VOID} - {participant.player for participant in match.participants}
    if free_player_slots:
        participant = Participant(user_id=user_id, player=[*free_player_slots][0])
        match.participants.add(participant)
    else:
        raise GameIsFullException()

    add_match_to_user_in_cache(user_id, match_id, game_type)

    return MatchDto.from_match(match, user_id)


def make_player_move(user_id: int, player_move: PlayerMoveDto, game_type: SaveType) -> MatchDto:
    num_of_mines = 10

    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")

    match: Match | None = get_match_by_user_id_from_cache(user_id, game_type)  # pyright: ignore[reportUnknownMemberType]
    if not match:
        raise GameNotFoundException()

    if match.state not in [MatchState.ACTIVE, MatchState.READY]:
        raise InvalidGameStateException()

    game = match.game
    action_type = ActionType[player_move.action_type]
    action_coordinates = Coordinates(**player_move.coordinates)
    player = next((p.player for p in match.participants if user_id == p.user_id))

    if not game.board.get(action_coordinates):
        raise InvalidPlayerMoveException()

    if match.state == MatchState.READY:
        populate_with_mines(game.board, num_of_mines, action_coordinates=[action_coordinates])
        match.state = MatchState.ACTIVE

    handle_player_step(match.game, action_type, action_coordinates, player)

    if check_for_finish(game):
        match.state = MatchState.FINISHED
        winning_player = check_for_winner(game)

        match.winner = next((
            participant
            for participant in match.participants
            if winning_player == participant.player
            ), None)
        remove_match_from_cache(match, game_type)  # pyright: ignore[reportUnknownMemberType]
    else:
        save_match_to_cache(match, game_type)  # pyright: ignore[reportUnknownMemberType]

    return MatchDto.from_match(match, user_id)
