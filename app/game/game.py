from dataclasses import dataclass
from enum import Enum, auto
from app.error_handling.exceptions import InvalidCellException


class Player(Enum):
    PLAYER_VOID = auto()
    PLAYER_ONE = auto()
    PLAYER_TWO = auto()
    PLAYER_THREE = auto()
    PLAYER_FOUR = auto()
    PLAYER_FIVE = auto()
    PLAYER_SIX = auto()
    PLAYER_SEVEN = auto()
    PLAYER_EIGHT = auto()


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
    def __init__(self,
                 *,
                 board: dict[Coordinates, "Cell"] = {},
                 players: set[Player] = set()
                 ):
        self.players = players
        self.board = board


class Cell:
    def __init__(self,
                 game: Game,
                 *,
                 is_mine: bool = False,
                 neighbors: set["Cell"] | None = None,
                 flagged_by: set[Player] | None = None,
                 owner: Player | None = None
                 ):
        self.game = game
        self.is_mine = is_mine
        self.neighbors = neighbors or set()
        self.flagged_by = flagged_by or set()
        self._owner: Player | None = owner
        self.num_neighbor_mines = 0

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner: Player):
        if owner not in self.game.players:
            raise InvalidCellException()
        self._owner = owner
