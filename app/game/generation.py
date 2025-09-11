from app.error_handling.exceptions import InvalidMapException
from .models import Coordinates, Game, Cell
from random import choice


def generate_game(num_of_rows: int, num_of_columns: int) -> Game:
    if num_of_rows < 1 or num_of_columns < 1:
        raise InvalidMapException()

    cells: dict[Coordinates, Cell] = {}
    game = Game(num_of_rows, num_of_columns, cells)

    for x in range(num_of_columns):
        for y in range(num_of_rows):
            cell = Cell(game, False, [])
            cells[Coordinates(x, y)] = cell

    for cell_coor, cell in cells.items():
        neighbors = [other_cell for other_coor, other_cell in cells.items() if __is_neighbor(cell_coor, other_coor)]
        cell.neighbors = neighbors

    game.cells = cells

    return game


def populate_with_mines(cells: dict[Coordinates, Cell], start_position: Coordinates, num_of_mines: int):
    valid_cells = [
        cell
        for cell_coor, cell in cells.items()
        if not __is_neighbor(start_position, cell_coor) and start_position != cell_coor
        ]

    if len(valid_cells) < num_of_mines:
        raise InvalidMapException()

    for _ in range(num_of_mines):
        cell = choice(valid_cells)
        cell.is_mine = True
        valid_cells.remove(cell)
        for neighbor in cell.neighbors:
            neighbor.num_neighbor_mines += 1


def __is_neighbor(coordinates_1: Coordinates, coordinates_2: Coordinates) -> bool:
    (x_1, y_1) = coordinates_1.get_coordinates()
    (x_2, y_2) = coordinates_2.get_coordinates()
    return abs(x_1 - x_2) <= 1 and abs(y_1 - y_2) <= 1 and coordinates_1 != coordinates_2
