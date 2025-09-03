from flask_sqlalchemy import SQLAlchemy
from app.custom_flask import CustomFlask
import os
from dotenv import load_dotenv


def init_db(app: CustomFlask, db: SQLAlchemy):
    load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
