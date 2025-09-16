from unittest.mock import MagicMock
import pytest
from app.error_handling.exceptions import InvalidPlayerMoveException
from app.game.gameplay import handle_player_step
from app.game.generation import generate_base_game_board
from app.game.models import ActionType, Coordinates, GameState


@pytest.fixture(autouse=True)
def populate_with_mines_mock(monkeypatch: pytest.MonkeyPatch):
    mock = MagicMock()
    monkeypatch.setattr("app.game.gameplay.populate_with_mines", mock)
    return mock


@pytest.fixture(autouse=True)
def num_of_mines_mock(monkeypatch: pytest. MonkeyPatch):
    mock = 10
    monkeypatch.setattr("app.game.gameplay.NUM_OF_MINES", mock)
    return mock


@pytest.fixture()
def handle_reveal_mock(monkeypatch: pytest.MonkeyPatch):
    mock = MagicMock()
    monkeypatch.setattr("app.game.gameplay.__handle_reveal_action", mock)
    return mock


@pytest.fixture()
def handle_flag_mock(monkeypatch: pytest.MonkeyPatch):
    mock = MagicMock()
    monkeypatch.setattr("app.game.gameplay.__handle_flag_action", mock)
    return mock


@pytest.fixture()
def reveal_cell_block_mock(monkeypatch: pytest.MonkeyPatch):
    mock = MagicMock()
    monkeypatch.setattr("app.game.gameplay.__reveal_cell_block", mock)
    return mock


def test__handle_player_step__action_cell_not_exist__raise_InvalidPlayerMoveException():
    game = generate_base_game_board(4, 4)
    action_coordinates = Coordinates(5, 5)

    with pytest.raises(InvalidPlayerMoveException) as exc_info:
        handle_player_step(game, ActionType.FLAG, action_coordinates)

    assert "GAME_INVALID_PLAYER_MOVE" == exc_info.value.errors[0].code


def test__handle_player_step__action_cell_not_hidden__raise_InvalidPlayerMoveException():
    game = generate_base_game_board(4, 4)
    action_coordinates = Coordinates(0, 0)
    game.cells[action_coordinates].is_hidden = False

    with pytest.raises(InvalidPlayerMoveException) as exc_info:
        handle_player_step(game, ActionType.FLAG, action_coordinates)

    assert "GAME_INVALID_PLAYER_MOVE" == exc_info.value.errors[0].code


def test__handle_player_step__action_type_reveal__run_handle_reveal_action(handle_reveal_mock: MagicMock, handle_flag_mock: MagicMock):
    game = generate_base_game_board(4, 4)
    action_type = ActionType.REVEAL
    action_coordinates = Coordinates(0, 0)

    handle_player_step(game, action_type, action_coordinates)

    handle_reveal_mock.assert_called_once_with(game, action_coordinates)
    handle_flag_mock.assert_not_called()


def test__handle_player_step__action_type_flag__run_handle_flag_action(handle_reveal_mock: MagicMock, handle_flag_mock: MagicMock):
    game = generate_base_game_board(4, 4)
    action_type = ActionType.FLAG
    action_coordinates = Coordinates(0, 0)

    handle_player_step(game, action_type, action_coordinates)

    handle_flag_mock.assert_called_once_with(game, action_coordinates)
    handle_reveal_mock.assert_not_called()


def test__handle_player_step__action_type_reveal_and_game_state_initialized__run_populate_mines_and_game_state_set_started(populate_with_mines_mock: MagicMock, num_of_mines_mock: int):
    game = generate_base_game_board(4, 4)
    game.state = GameState.INITIALIZED
    action_type = ActionType.REVEAL
    action_coordinates = Coordinates(0, 0)

    handle_player_step(game, action_type, action_coordinates)

    populate_with_mines_mock.assert_called_once_with(game.cells, action_coordinates, num_of_mines_mock)


def test__handle_player_step__action_type_reveal_and_action_cell_mine__game_state_set_finished_lost_and_reveal_cell_block_not_run(reveal_cell_block_mock: MagicMock):
    game = generate_base_game_board(4, 4)
    action_type = ActionType.REVEAL
    action_coordinates = Coordinates(0, 0)
    game.cells[action_coordinates].is_mine = True

    handle_player_step(game, action_type, action_coordinates)

    reveal_cell_block_mock.assert_not_called()
    assert GameState.FINISHED_LOST == game.state


def test__handle_player_step__action_type_reveal_and_action_cell_not_mine__reveal_cell_block_run(reveal_cell_block_mock: MagicMock):
    game = generate_base_game_board(4, 4)
    action_type = ActionType.REVEAL
    action_coordinates = Coordinates(0, 0)
    action_cell = game.cells[action_coordinates]
    action_cell.is_mine = False

    handle_player_step(game, action_type, action_coordinates)

    reveal_cell_block_mock.assert_called_once_with(game, action_cell)


def test__handle_player_step__action_type_reveal_and_player_won__reveal_cell_block_run_and_game_state_set_finished_won(reveal_cell_block_mock: MagicMock):
    game = generate_base_game_board(4, 4)
    action_type = ActionType.REVEAL
    action_coordinates = Coordinates(0, 0)
    action_cell = game.cells[action_coordinates]
    action_cell.is_mine = False
    for cell in game.cells.values():
        cell.is_hidden = False
    action_cell.is_hidden = True

    handle_player_step(game, action_type, action_coordinates)

    reveal_cell_block_mock.assert_called_once_with(game, action_cell)
    assert GameState.FINISHED_WON == game.state


def test__handle_player_step__action_type_flag_and_action_cell_flagged__unflag_cell():
    game = generate_base_game_board(4, 4)
    action_type = ActionType.FLAG
    action_coordinates = Coordinates(0, 0)
    game.cells[action_coordinates].is_flagged = True

    handle_player_step(game, action_type, action_coordinates)

    assert False == game.cells[action_coordinates].is_flagged


def test__handle_player_step__action_type_flag_and_action_cell_unflagged__flag_cell():
    game = generate_base_game_board(4, 4)
    action_type = ActionType.FLAG
    action_coordinates = Coordinates(0, 0)
    game.cells[action_coordinates].is_flagged = False

    handle_player_step(game, action_type, action_coordinates)

    assert True == game.cells[action_coordinates].is_flagged
