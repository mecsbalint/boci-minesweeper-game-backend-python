from unittest.mock import MagicMock, patch
import pytest
from app.database.db_models import User
from app.dto.game_dto import GameDto, PlayerMoveDto
from app.error_handling.exceptions import UserNotFoundException, GameNotFoundException
from app.game.models import ActionType, Coordinates, Game, GameState
from app.service.game_service import create_game, check_active_game, get_active_game, make_player_move


@pytest.fixture
def user():
    user = User("John Doe", "johndoe@email.com", "johnDO3")
    user.id = 1
    return user


@pytest.fixture
def game():
    game = Game(10, 10, {})
    game.state = GameState.INITIALIZED
    return game


@pytest.fixture
def player_move_dto():
    return PlayerMoveDto(coordinates={"x": 1, "y": 1}, action_type="REVEAL")


@patch("app.service.game_service.get_user_by_id")
@patch("app.service.game_service.generate_game")
@patch("app.service.game_service.cache")
def test__create_game__user_exist__game_generated_and_saved_in_cache(cache_mock: MagicMock, generate_game_mock: MagicMock, get_user_mock: MagicMock, user: User, game: Game):
    get_user_mock.return_value = user
    generate_game_mock.return_value = game
    user_id = 1

    create_game(user_id)
    cache_arg_user_id, cache_arg_game = cache_mock.set.call_args[0]

    generate_game_mock.assert_called_once()
    cache_mock.set.assert_called_once()
    assert cache_arg_user_id == user_id
    assert cache_arg_game == game


@patch("app.service.game_service.get_user_by_id")
def test__create_game__user_not_exist__raise_UserNotFoundException(get_user_mock: MagicMock):
    get_user_mock.return_value = None

    with pytest.raises(UserNotFoundException) as exc_info:
        create_game(1)

    assert "USER_NOT_FOUND" == exc_info.value.errors[0].code


@patch("app.service.game_service.get_user_by_id")
@patch("app.service.game_service.cache")
def test__check_active_game__user_exist__return_cache_has_value(cache_mock: MagicMock, get_user_mock: MagicMock, user: User):
    get_user_mock.return_value = user
    cache_mock.has.return_value = False
    user_id = 1

    expected_result = False
    actual_result = check_active_game(user_id)
    cache_arg_user_id = cache_mock.has.call_args[0][0]

    cache_mock.has.assert_called_once()
    assert cache_arg_user_id == user_id
    assert expected_result == actual_result


@patch("app.service.game_service.get_user_by_id")
def test__check_active_game__user_not_exist__raise_UserNotFoundException(get_user_mock: MagicMock):
    get_user_mock.return_value = None

    with pytest.raises(UserNotFoundException) as exc_info:
        check_active_game(1)

    assert "USER_NOT_FOUND" == exc_info.value.errors[0].code


@patch("app.service.game_service.get_user_by_id")
@patch("app.service.game_service.cache")
def test__get_active_game__user_exist_game_exist__return_GameDto(cache_mock: MagicMock, get_user_mock: MagicMock, user: User, game: Game):
    get_user_mock.return_value = user
    cache_mock.get.return_value = game

    expected_result = GameDto.from_game(game)
    actual_result = get_active_game(1)

    assert expected_result == actual_result


@patch("app.service.game_service.get_user_by_id")
def test__get_active_game__user_not_exist__raise_UserNotFoundException(get_user_mock: MagicMock):
    get_user_mock.return_value = None

    with pytest.raises(UserNotFoundException) as exc_info:
        get_active_game(1)

    assert "USER_NOT_FOUND" == exc_info.value.errors[0].code


@patch("app.service.game_service.get_user_by_id")
@patch("app.service.game_service.cache")
def test__get_active_game__user_exist_game_not_exist__raise_GameNotFoundException(cache_mock: MagicMock, get_user_mock: MagicMock, user: User):
    get_user_mock.return_value = user
    cache_mock.get.return_value = None

    with pytest.raises(GameNotFoundException) as exc_info:
        get_active_game(1)

    assert "GAME_NOT_FOUND" == exc_info.value.errors[0].code


@patch("app.service.game_service.get_user_by_id")
@patch("app.service.game_service.cache")
@patch("app.service.game_service.handle_player_step")
def test__make_player_move__user_exist_game_exist_and_not_finished__call_cahce_set_and_return_GameDto(handle_player_step_mock: MagicMock, cache_mock: MagicMock, get_user_mock: MagicMock, user: User, game: Game, player_move_dto: PlayerMoveDto):
    get_user_mock.return_value = user
    cache_mock.get.return_value = game
    user_id = 1

    expected_result = GameDto.from_game(game)
    actual_result = make_player_move(user_id, player_move_dto)
    handle_player_step_arg_game, handle_player_step_arg_action_type, handle_player_step_arg_action_coordinates = handle_player_step_mock.call_args[0]
    cache_arg_user_id, cache_arg_game = cache_mock.set.call_args[0]

    handle_player_step_mock.assert_called_once()
    cache_mock.set.assert_called_once()
    assert handle_player_step_arg_game == game
    assert handle_player_step_arg_action_type == ActionType[player_move_dto.action_type]
    assert handle_player_step_arg_action_coordinates == Coordinates(**player_move_dto.coordinates)
    assert cache_arg_user_id == user_id
    assert cache_arg_game == game
    assert expected_result == actual_result


@patch("app.service.game_service.get_user_by_id")
@patch("app.service.game_service.cache")
@patch("app.service.game_service.handle_player_step")
def test__make_player_move__user_exist_game_exist_and_finished__call_cahce_delete_and_return_GameDto(handle_player_step_mock: MagicMock, cache_mock: MagicMock, get_user_mock: MagicMock, user: User, game: Game, player_move_dto: PlayerMoveDto):
    get_user_mock.return_value = user
    cache_mock.get.return_value = game
    user_id = 1
    game.state = GameState.FINISHED_WON

    expected_result = GameDto.from_game(game)
    actual_result = make_player_move(user_id, player_move_dto)
    handle_player_step_arg_game, handle_player_step_arg_action_type, handle_player_step_arg_action_coordinates = handle_player_step_mock.call_args[0]
    cache_arg_user_id = cache_mock.delete.call_args[0][0]

    handle_player_step_mock.assert_called_once()
    cache_mock.delete.assert_called_once()
    assert handle_player_step_arg_game == game
    assert handle_player_step_arg_action_type == ActionType[player_move_dto.action_type]
    assert handle_player_step_arg_action_coordinates == Coordinates(**player_move_dto.coordinates)
    assert cache_arg_user_id == user_id
    assert expected_result == actual_result


@patch("app.service.game_service.get_user_by_id")
def test__make_player_move__user_not_exist__raise_UserNotFoundException(get_user_mock: MagicMock, player_move_dto: PlayerMoveDto):
    get_user_mock.return_value = None

    with pytest.raises(UserNotFoundException) as exc_info:
        make_player_move(1, player_move_dto)

    assert "USER_NOT_FOUND" == exc_info.value.errors[0].code


@patch("app.service.game_service.get_user_by_id")
@patch("app.service.game_service.cache")
def test__make_player_move__user_exist_game_not_exist__raise_GameNotFoundException(cache_mock: MagicMock, get_user_mock: MagicMock, user: User, player_move_dto: PlayerMoveDto):
    get_user_mock.return_value = user
    cache_mock.get.return_value = None

    with pytest.raises(GameNotFoundException) as exc_info:
        make_player_move(1, player_move_dto)

    assert "GAME_NOT_FOUND" == exc_info.value.errors[0].code
