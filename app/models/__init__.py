from .user import init_user


def init_models(db):
    init_user(db)
