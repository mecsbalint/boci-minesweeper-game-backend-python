from dataclasses import dataclass
from enum import Enum, auto
from app.error_handling.exceptions import InvalidCellException


class Player(Enum):
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    PLAYER_THREE = 2
    PLAYER_FOUR = 3
    PLAYER_FIVE = 4
    PLAYER_SIX = 5
    PLAYER_SEVEN = 6
    PLAYER_EIGHT = 7
    PLAYER_VOID = 8


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
