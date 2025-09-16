from functools import reduce
from unittest.mock import MagicMock, patch
import pytest
from app.error_handling.exceptions import InvalidBoardException
from app.game.generation import generate_base_game_board, populate_with_mines
from app.game.models import Cell, Coordinates


def test__generate_game__return_game_with_right_num_of_cells():
    game = generate_base_game_board(4, 4)

    assert len(game.cells) == game.rows * game.columns


def test__generate_game__return_game_with_cells_with_right_coordinates():
    game = generate_base_game_board(4, 4)
    coordinates_tuples_iterable = [coor.get_coordinates() for coor in game.cells.keys()]

    for y in range(game.rows):
        for x in range(game.columns):
            assert (x, y) in coordinates_tuples_iterable


def test__generate_game__return_game_with_cells_with_right_num_of_neighbors():
    game = generate_base_game_board(4, 4)

    for coor, cell in game.cells.items():
        x, y = coor.get_coordinates()
        if 0 < x < (game.columns - 1) and 0 < y < (game.rows - 1):
            assert len(cell.neighbors) == 8
        elif 0 < x < (game.columns - 1) or 0 < y < (game.rows - 1):
            assert len(cell.neighbors) == 5
        else:
            assert len(cell.neighbors) == 3


def test__generate_game__invalid_num_of_rows__raise_InvalidMapException():
    num_of_rows = -1
    num_of_columns = 8

    with pytest.raises(InvalidBoardException) as exc_info:
        generate_base_game_board(num_of_rows, num_of_columns)

    assert "GAME_MAP_ERROR" == exc_info.value.errors[0].code


@patch("app.game.generation.choice")
def test__populate_with_mines__start_position_and_neighbors_has_mine_false(choice_mock: MagicMock):
    choice_mock.side_effect = lambda seq: seq[0]  # pyright: ignore[reportUnknownLambdaType]
    game = generate_base_game_board(4, 4)
    start_coordinates = Coordinates(0, 0)
    start_cell = game.cells[start_coordinates]
    neighbors = start_cell.neighbors
    num_of_mines = 12

    populate_with_mines(game.cells, start_coordinates, num_of_mines)

    assert not start_cell.is_mine
    assert all(not n.is_mine for n in neighbors)


@patch("app.game.generation.choice")
def test__populate_with_mines__correct_num_of_mines_placed(choice_mock: MagicMock):
    choice_mock.side_effect = lambda seq: seq[0]  # pyright: ignore[reportUnknownLambdaType]
    cells = generate_base_game_board(4, 4).cells
    start_coordinates = Coordinates(0, 0)
    num_of_mines = 12

    populate_with_mines(cells, start_coordinates, num_of_mines)
    actual_num_of_mines = reduce(lambda agg, cell: agg + (1 if cell.is_mine else 0), cells.values(), 0)

    assert num_of_mines == actual_num_of_mines


@patch("app.game.generation.choice")
def test__populate_with_mines__num_neighbor_mines_correspond_with_neighbor_mines_number(choice_mock: MagicMock):
    choice_mock.side_effect = lambda seq: seq[0]  # pyright: ignore[reportUnknownLambdaType]
    choice_mock.side_effect = lambda seq: seq[0]  # pyright: ignore[reportUnknownLambdaType]
    cells = generate_base_game_board(4, 4).cells
    start_coordinates = Coordinates(0, 0)
    num_of_mines = 12

    populate_with_mines(cells, start_coordinates, num_of_mines)

    assert all(cell.num_neighbor_mines == reduce(
        lambda agg, cell: agg + (1 if cell.is_mine else 0),
        cell.neighbors,
        0
        )
        for cell in cells.values())


def test__populate_with_mines__there_is_no_enough_valid_cells__raise_InvalidMapException():
    empty_cells_dict: dict[Coordinates, Cell] = {}

    with pytest.raises(InvalidBoardException) as exc_info:
        populate_with_mines(empty_cells_dict, Coordinates(0, 0), 10)

    assert "GAME_MAP_ERROR" == exc_info.value.errors[0].code
