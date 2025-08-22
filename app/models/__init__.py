from .user import User


def create_tables(app, db):
    with app.app_context():
        db.drop_all()
        db.create_all()
