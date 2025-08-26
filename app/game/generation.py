from .models import Game, Cell
from random import choice

NUM_OF_ROWS = 10
NUM_OF_COLUMNS = 10
NUM_OF_MINES = 5


def generate_game() -> Game:
    cells = []
    game = Game(NUM_OF_ROWS, NUM_OF_COLUMNS, cells)

    for x in range(NUM_OF_COLUMNS):
        for y in range(NUM_OF_ROWS):
            cell = Cell(game, (x, y), False, [])
            cells.append(cell)

    for cell_1 in cells:
        neighbors = [cell_2 for cell_2 in cells if is_neighbor(cell_1, cell_2)]
        cell.neighbors = neighbors

    game.cells = cells

    return game


def populate_with_mines(cells: list[Cell], start_position: Cell):
    cells = [cell for cell in list(cells) if not is_neighbor(start_position, cell) and start_position is not cell]

    for x in range(NUM_OF_MINES):
        cell = choice(cells)
        cell.is_mine = True
        cells.remove(cell)


def is_neighbor(cell_1: Cell, cell_2: Cell) -> bool:
    (x_1, y_1) = cell_1.coordinates
    (x_2, y_2) = cell_2.coordinates
    return (x_1 - x_2) * -1 in [0, 1] and (y_1 - y_2) * -1 in [0, 1] and cell_1 is not cell_2
