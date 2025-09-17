from dataclasses import dataclass
from enum import Enum, auto
from app.error_handling.exceptions import InvalidCellException, InvalidMapException


class Player(Enum):
    PLAYER_VOID = (0, False)
    PLAYER_ONE = (1, True)
    PLAYER_TWO = (2, True)

    def __init__(self, num: int, active: bool) -> None:
        self.num = num
        self.active = active


class GameState(Enum):
    CREATED = auto(),
    WAITING = auto(),
    READY = auto(),
    ACTIVE = auto(),
    FINISHED = auto()


class ActionType(Enum):
    REVEAL = auto()
    FLAG = auto()


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int

    def get_coordinates(self) -> tuple[int, int]:
        return (self.x, self.y)


class Game:
    def __init__(self, players: set[Player], num_of_mines: int, *, board: dict[Coordinates, "Cell"] = {}, winner: Player | None = None):
        self.state: GameState = GameState.CREATED
        self._winner = winner
        self.players = players
        self.board = board
        self.num_of_mines = num_of_mines

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, winner: Player | None):
        if self.state is not GameState.FINISHED:
            raise InvalidMapException()
        self._winner = winner


class Cell:
    def __init__(self, game: Game, *, is_mine: bool = False, neighbors: set["Cell"] = set(), flagged_by: set[Player] = set(), owner: Player | None = None):
        self.game = game
        self.is_mine = is_mine
        self.neighbors = neighbors
        self.flagged_by = flagged_by
        self._owner: Player | None = owner
        self.num_neighbor_mines = 0

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner: Player):
        if self.is_mine:
            raise InvalidCellException()
        self._owner = owner
