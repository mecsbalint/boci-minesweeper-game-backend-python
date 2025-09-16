from app.error_handling.exceptions import InvalidBoardException
from .models import Coordinates, Game, Cell
from random import choice


def generate_base_game_board(game: Game, num_of_rows: int, num_of_columns: int) -> dict[Coordinates, Cell]:
    if num_of_rows < 1 or num_of_columns < 1:
        raise InvalidBoardException()

    board: dict[Coordinates, Cell] = {}

    for x in range(num_of_columns):
        for y in range(num_of_rows):
            cell = Cell(game)
            board[Coordinates(x, y)] = cell

    for cell_coor, cell in board.items():
        neighbors = {other_cell for other_coor, other_cell in board.items() if __is_neighbor(cell_coor, other_coor)}
        cell.neighbors = neighbors

    return board


def populate_with_mines(board: dict[Coordinates, Cell], start_positions: set[Coordinates], num_of_mines: int):
    valid_cells = [
        cell
        for coor, cell in board.items()
        if not __is_neighbor_of_any(coor, start_positions) and coor not in start_positions
        ]

    if len(valid_cells) < num_of_mines:
        raise InvalidBoardException()

    for _ in range(num_of_mines):
        cell = choice(valid_cells)
        cell.is_mine = True
        valid_cells.remove(cell)
        for neighbor in cell.neighbors:
            neighbor.num_neighbor_mines += 1


def __is_neighbor_of_any(coordinates: Coordinates, candidate_coors: set[Coordinates]) -> bool:
    for candidate in candidate_coors:
        if __is_neighbor(coordinates, candidate):
            return True
    return False


def __is_neighbor(coordinates_1: Coordinates, coordinates_2: Coordinates) -> bool:
    (x_1, y_1) = coordinates_1.get_coordinates()
    (x_2, y_2) = coordinates_2.get_coordinates()
    return abs(x_1 - x_2) <= 1 and abs(y_1 - y_2) <= 1 and coordinates_1 != coordinates_2
