from flask_sqlalchemy import SQLAlchemy
from app import CustomFlask


def create_tables(app: CustomFlask, db: SQLAlchemy):
    with app.app_context():
        db.drop_all()
        db.create_all()
