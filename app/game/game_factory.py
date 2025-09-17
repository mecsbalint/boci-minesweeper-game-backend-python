from abc import ABC, abstractmethod
from app.error_handling.exceptions import InvalidBoardException
from app.game.game import Coordinates, Game, Cell


class GameFactory(ABC):

    @abstractmethod
    def create_game(self) -> Game:
        pass


class GridGameFactory(GameFactory, ABC):

    @staticmethod
    def _is_neighbor(coordinates_1: Coordinates, coordinates_2: Coordinates) -> bool:
        (x_1, y_1) = coordinates_1.get_coordinates()
        (x_2, y_2) = coordinates_2.get_coordinates()
        return abs(x_1 - x_2) <= 1 and abs(y_1 - y_2) <= 1 and coordinates_1 != coordinates_2


class RectangularGameFactory(GridGameFactory):

    def __init__(self, num_of_rows: int, num_of_columns: int) -> None:
        self.num_of_rows = num_of_rows
        self.num_of_columns = num_of_columns

    def create_game(self) -> Game:
        if self.num_of_rows < 1 or self.num_of_columns < 1:
            raise InvalidBoardException()

        game = Game()
        board: dict[Coordinates, Cell] = {}

        for x in range(self.num_of_columns):
            for y in range(self.num_of_rows):
                cell = Cell(game)
                board[Coordinates(x, y)] = cell

        for cell_coor, cell in board.items():
            neighbors = {
                other_cell
                for other_coor, other_cell in board.items()
                if self._is_neighbor(cell_coor, other_coor)
                }
            cell.neighbors = neighbors

        game.board = board

        return game
