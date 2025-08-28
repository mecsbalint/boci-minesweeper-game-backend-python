from typing import cast
from app.extensions import db
from app.database.db_models import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash


def validate_user(email: str, password: str) -> tuple[str, str] | None:
    user = get_user_by_email(email)
    if user:
        is_password_valid = check_password_hash(user.password, password)
        if is_password_valid:
            return (user.id, user.name)
    return None


def get_user_by_email(email: str) -> User | None:
    user = cast(User | None, User.query.filter_by(email=email).first())
    return user


def get_user_by_id(id: int) -> User | None:
    user = cast(User | None, User.query.filter_by(id=id).first())
    return user


def create_user(name: str, email: str, password: str) -> bool:
    try:
        password_hashed = generate_password_hash(password)
        user_new = User(name, email, password_hashed)
        db.session.add(user_new)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        print("Constraint violated while saving User")
        return False
