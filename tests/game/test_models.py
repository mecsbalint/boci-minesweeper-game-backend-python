from copy import copy
import pytest
from app.error_handling.exceptions import InvalidBoardException
from app.game.generation import __generate_base_game_board
from app.game.models import Cell, Coordinates, Game

@pytest.fixture
def game():
    return __generate_base_game_board(4, 4)


def test__Game__set_cells_mismatched_number_of_cells__raise_InvalidMapException(game: Game):
    valid_coordinates = Coordinates(0, 0)
    cells = {valid_coordinates: Cell(game, False, [])}

    with pytest.raises(InvalidBoardException) as exc_info:
        game.cells = cells

    assert "GAME_MAP_ERROR" == exc_info.value.errors[0].code


def test__Game__set_cells_one_cell_has_invalid_coordinates__raise_InvalidMapException(game: Game):
    invalid_coordinates = Coordinates(5, 5)
    valid_coordinates = Coordinates(0, 0)
    cells = copy(game.cells)
    cells.pop(valid_coordinates)
    cells[invalid_coordinates] = Cell(game, False, [])

    with pytest.raises(InvalidBoardException) as exc_info:
        game.cells = cells

    assert "GAME_MAP_ERROR" == exc_info.value.errors[0].code


def test__Game__set_cells_all_cells_have_invalid_coordinates__raise_InvalidMapException(game: Game):
    invalid_coordinates = Coordinates(5, 5)
    cells = {invalid_coordinates: Cell(game, False, []) for _ in range(len(game.cells))}

    with pytest.raises(InvalidBoardException) as exc_info:
        game.cells = cells

    assert "GAME_MAP_ERROR" == exc_info.value.errors[0].code


def test__Game__set_cells_all_cells_have_valid_coordinates__cells_added_to_game(game: Game):
    valid_coordinate = Coordinates(0, 0)
    cell = Cell(game, False, [])
    cells = copy(game.cells)
    cells[valid_coordinate] = cell

    game.cells = cells

    assert cells is game.cells
