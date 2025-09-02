from .models import Coordinates, Game, Cell
from random import choice

NUM_OF_ROWS = 8
NUM_OF_COLUMNS = 8
NUM_OF_MINES = 10


def generate_game() -> Game:
    cells: dict[Coordinates, Cell] = {}
    game = Game(NUM_OF_ROWS, NUM_OF_COLUMNS, cells)

    for x in range(NUM_OF_COLUMNS):
        for y in range(NUM_OF_ROWS):
            cell = Cell(game, False, [])
            cells[Coordinates(x, y)] = cell

    for cell_coor, cell in cells.items():
        neighbors = [other_cell for other_coor, other_cell in cells.items() if __is_neighbor(cell_coor, other_coor)]
        cell.neighbors = neighbors

    game.cells = cells

    return game


def populate_with_mines(cells: dict[Coordinates, Cell], start_position: Coordinates):
    valid_cells = [
        cell
        for cell_coor, cell in cells.items()
        if not __is_neighbor(start_position, cell_coor) and start_position != cell_coor
        ]

    for _ in range(NUM_OF_MINES):
        cell = choice(valid_cells)
        cell.is_mine = True
        valid_cells.remove(cell)

    for cell in cells.values():
        cell.num_neighbor_mines = cell.count_neighbor_mines()


def __is_neighbor(coordinates_1: Coordinates, coordinates_2: Coordinates) -> bool:
    (x_1, y_1) = coordinates_1.get_coordinates()
    (x_2, y_2) = coordinates_2.get_coordinates()
    return abs(x_1 - x_2) <= 1 and abs(y_1 - y_2) <= 1 and coordinates_1 != coordinates_2
