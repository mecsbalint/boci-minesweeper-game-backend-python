from dataclasses import dataclass
from enum import Enum, auto

from app.error_handling.exceptions import InvalidMapException


class GameState(Enum):
    INITIALIZED = auto()
    STARTED = auto()
    FINISHED_LOST = auto()
    FINISHED_WON = auto()


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
    def __init__(self, rows: int, columns: int, cells: dict[Coordinates, "Cell"]):
        self.rows = rows
        self.columns = columns
        self._cells = cells
        self.state: GameState = GameState.INITIALIZED

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, cells: dict[Coordinates, "Cell"]):
        if len(cells) != self.rows * self.columns:
            raise InvalidMapException()
        for coor, cell in cells.items():
            if (not (0 <= coor.x <= self.rows and 0 <= coor.y <= self.columns)):
                raise InvalidMapException()


class Cell:
    def __init__(self, game: Game, is_mine: bool, neighbors: list["Cell"]):
        self.game = game
        self.is_mine = is_mine
        self.neighbors = neighbors
        self.is_hidden = True
        self.is_flagged = False
        self.num_neighbor_mines = 0
