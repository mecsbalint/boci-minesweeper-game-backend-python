from typing import Callable, ParamSpec, TypeVar
from typing import cast
from app.dto.user_dto import UserDto
from app.error_handling.exceptions import InvalidPasswordException, UserNotFoundException, UserAlreadyExistException
from app.extensions import db
from app.database.db_models import User
from werkzeug.security import check_password_hash, generate_password_hash

R = TypeVar("R")
P = ParamSpec("P")


def with_app_context(func: Callable[P, R]) -> Callable[P, R]:

    def with_app_context_wrapper(*args: P.args, **kwargs: P.kwargs):
        from app import flask_app
        with flask_app.app_context():
            return func(*args, **kwargs)
    return with_app_context_wrapper


def validate_user(email: str, password: str) -> UserDto:
    user = get_user_by_email(email)
    if user:
        is_password_valid = check_password_hash(user.password, password)
        if is_password_valid:
            return UserDto(id=user.id, name=user.name)
        else:
            raise InvalidPasswordException()
    else:
        raise UserNotFoundException("e-mail")


@with_app_context
def get_user_by_email(email: str) -> User | None:
    user = cast(User | None, User.query.filter_by(email=email).first())
    return user


@with_app_context
def get_user_by_id(id: int) -> User | None:
    user = cast(User | None, User.query.filter_by(id=id).first())
    return user


@with_app_context
def create_user(name: str, email: str, password: str) -> None:
    if get_user_by_email(email):
        raise UserAlreadyExistException()
    password_hashed = generate_password_hash(password)
    user_new = User(name, email, password_hashed)
    db.session.add(user_new)
    db.session.commit()
