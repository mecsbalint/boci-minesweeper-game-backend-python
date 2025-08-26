from app.extensions import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash


def validate_user(email, password):
    user = get_user_by_email(email)

    return user.name if user and check_password_hash(user.password, password) else None


def get_user_by_email(email) -> User | None:
    user = User.query.filter_by(email=email).first()
    return user


def create_user(name, email, password):
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
