from app.cache.match_cache import save_match_to_cache
from app.error_handling.exceptions import InvalidBoardException, UserNotFoundException
from app.game.game import Coordinates, Player
from app.game.game_factory import RectangularGameFactory
from app.game.match import Match, MatchState, Participant
from game.gameplay import populate_with_mines, get_cell_block, remove_mines
from app.service.user_service import get_user_by_id


NUM_OF_ROWS = 15
NUM_OF_COLUMNS = 15
NUM_OF_MINES = 12
NUM_OF_PLAYERS = 2
START_POSITIONS = [Coordinates(3, 8), Coordinates(12, 8)]


def create_game(user_id: int):
    if not get_user_by_id(user_id):
        raise UserNotFoundException("id")

    gameFactory = RectangularGameFactory(NUM_OF_ROWS, NUM_OF_COLUMNS)
    game = gameFactory.create_game()

    for _ in range(10):

        populate_with_mines(game.board, NUM_OF_MINES, action_coordinates=START_POSITIONS)

        if game.board.get(START_POSITIONS[1]) in get_cell_block(game, START_POSITIONS[0]):
            remove_mines(game.board)
            continue

        game.players = {*list(Player)[:NUM_OF_PLAYERS]}
        participants = {Participant(user_id=user_id, player=Player.PLAYER_ONE)}
        match = Match(game, participants=participants)
        match.state = MatchState.WAITING
        save_match_to_cache(match, "MP")
        return None

    raise InvalidBoardException()
