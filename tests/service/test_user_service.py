from app.database.db_models import User
from app.dto.user_dto import UserDto
from app.error_handling.exceptions import InvalidPasswordException, UserNotFoundException, UserAlreadyExistException
from app.service.user_service import validate_user, create_user
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture
def user():
    user = User("John Doe", "johndoe@email.com", "johnDO3")
    user.id = 1
    return user


@pytest.fixture
def user_dto():
    return UserDto(id=1, name="John Doe")


@patch("app.service.user_service.check_password_hash")
@patch("app.service.user_service.get_user_by_email")
def test__validate_user__user_exist_and_password_valid__return_UserDto(mock_get_user: MagicMock, mock_check_password: MagicMock, user: User, user_dto: UserDto):
    mock_get_user.return_value = user
    mock_check_password.return_value = True

    expected_value = user_dto
    actual_value = validate_user("email", "password")

    assert expected_value == actual_value


@patch("app.service.user_service.get_user_by_email")
def test_validate_user__user_not_exist__raise_UserNotFoundException(mock_get_user: MagicMock):
    mock_get_user.return_value = None

    with pytest.raises(UserNotFoundException) as exc_info:
        validate_user("email", "password")

    assert "USER_NOT_FOUND" == exc_info.value.errors[0].code


@patch("app.service.user_service.check_password_hash")
@patch("app.service.user_service.get_user_by_email")
def test__validate_user__user_exist_and_password_invalid__raise_InvalidPasswordException(mock_get_user: MagicMock, mock_check_password: MagicMock, user: User):
    mock_get_user.return_value = user
    mock_check_password.return_value = False

    with pytest.raises(InvalidPasswordException) as exc_info:
        validate_user("email", "password")

    assert "USER_INVALID_PASSWORD" == exc_info.value.errors[0].code


@patch("app.service.user_service.get_user_by_email")
@patch("app.service.user_service.generate_password_hash")
@patch("app.service.user_service.db")
def test__create_user__user_not_exist__save_user_to_database(mock_db: MagicMock, mock_generate_password: MagicMock, mock_get_user: MagicMock):
    mock_get_user.return_value = None
    mock_generate_password.return_value = "pswrd_hash"

    create_user("name", "email", "password")
    added_user = mock_db.session.add.call_args[0][0]

    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()
    assert added_user.name == "name"
    assert added_user.email == "email"
    assert added_user.password == "pswrd_hash"


@patch("app.service.user_service.get_user_by_email")
def test__create_user__user_exist__rase_UserAlreadyExistException(mock_get_user: MagicMock):
    mock_get_user.return_value = User("John Doe", "johndoe@email.com", "johnDO3")

    with pytest.raises(UserAlreadyExistException) as exc_info:
        create_user("name", "email", "password")

    assert "USER_EXIST" == exc_info.value.errors[0].code
