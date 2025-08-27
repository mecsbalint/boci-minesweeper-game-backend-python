from enum import Enum, auto


class GameState(Enum):
    INITIALIZED = auto()
    STARTED = auto()
    FINISHED_LOST = auto()
    FINISHED_WON = auto()


class ActionType(Enum):
    REVEAL = auto()
    FLAG = auto()


class Coordinates():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_coordinates(self) -> tuple:
        return (self.x, self.y)


class Game:
    def __init__(self, rows: int, columns: int, cells: dict[Coordinates, "Cell"]):
        self.rows = rows
        self.columns = columns
        self.cells = cells
        self.state = GameState.INITIALIZED


class Cell:
    def __init__(self, game: Game, is_mine: bool, neighbors: list["Cell"]):
        self.game = game
        self.is_mine = is_mine
        self.neighbors = neighbors
        self.is_hidden = True
        self.is_flagged = False
        self.num_neighbor_mines = self.count_neighbor_mines()

    def count_neighbor_mines(self) -> int:
        return len(filter(lambda cell: cell.is_mine, self.neighbors))
