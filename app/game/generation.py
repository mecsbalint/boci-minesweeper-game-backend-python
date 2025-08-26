from .models import Game, Cell
from random import choice


def create_Game(rows: int, columns: int) -> Game:
    cells = []
    game = Game(rows, columns, cells)

    for x in range(columns):
        for y in range(rows):
            cell = Cell(game, (x, y), False, [])
            cells.append(cell)

    for cell_1 in cells:
        neighbors = [cell_2 for cell_2 in cells if is_neighbor(cell_1, cell_2)]
        cell.neighbors = neighbors

    game.cells = cells

    return game


def populate_with_mines(cells: list[Cell], start_position: Cell, num_of_mines: int):
    cells = [cell for cell in list(cells) if not is_neighbor(start_position, cell)]

    for x in range(num_of_mines):
        cell = choice(cells)
        cell.is_mine = True
        cells.remove(cell)


def is_neighbor(cell_1: Cell, cell_2: Cell) -> bool:
    (x_1, y_1) = cell_1.coordinates
    (x_2, y_2) = cell_2.coordinates
    return (x_1 - x_2) * -1 in [0, 1] and (y_1 - y_2) * -1 in [0, 1]
