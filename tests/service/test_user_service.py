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
def test__validate_user__user_exist_and_password_valid__return_UserDto(get_user_mock: MagicMock, check_password_mock: MagicMock, user: User, user_dto: UserDto):
    get_user_mock.return_value = user
    check_password_mock.return_value = True

    expected_value = user_dto
    actual_value = validate_user("email", "password")

    assert expected_value == actual_value


@patch("app.service.user_service.get_user_by_email")
def test_validate_user__user_not_exist__raise_UserNotFoundException(get_user_mock: MagicMock):
    get_user_mock.return_value = None

    with pytest.raises(UserNotFoundException) as exc_info:
        validate_user("email", "password")

    assert "USER_NOT_FOUND" == exc_info.value.errors[0].code


@patch("app.service.user_service.check_password_hash")
@patch("app.service.user_service.get_user_by_email")
def test__validate_user__user_exist_and_password_invalid__raise_InvalidPasswordException(get_user_mock: MagicMock, check_password_mock: MagicMock, user: User):
    get_user_mock.return_value = user
    check_password_mock.return_value = False

    with pytest.raises(InvalidPasswordException) as exc_info:
        validate_user("email", "password")

    assert "USER_INVALID_PASSWORD" == exc_info.value.errors[0].code


@patch("app.service.user_service.get_user_by_email")
@patch("app.service.user_service.generate_password_hash")
@patch("app.service.user_service.db")
def test__create_user__user_not_exist__save_user_to_database(db_mock: MagicMock, generate_password_mock: MagicMock, get_user_mock: MagicMock):
    get_user_mock.return_value = None
    generate_password_mock.return_value = "pswrd_hash"

    create_user("name", "email", "password")
    added_user = db_mock.session.add.call_args[0][0]

    db_mock.session.add.assert_called_once()
    db_mock.session.commit.assert_called_once()
    assert added_user.name == "name"
    assert added_user.email == "email"
    assert added_user.password == "pswrd_hash"


@patch("app.service.user_service.get_user_by_email")
def test__create_user__user_exist__rase_UserAlreadyExistException(get_user_mock: MagicMock):
    get_user_mock.return_value = User("John Doe", "johndoe@email.com", "johnDO3")

    with pytest.raises(UserAlreadyExistException) as exc_info:
        create_user("name", "email", "password")

    assert "USER_EXIST" == exc_info.value.errors[0].code
