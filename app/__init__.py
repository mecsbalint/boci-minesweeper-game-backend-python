from flask import Flask
from app.controllers import init_endpoints
from app.extensions import db
from app.database import create_tables
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from app.security.jwt import init_flask_jwt  # pyright: ignore[reportUnknownVariableType]
from app.services.game_session_manager import GameSessionManager


class CustomFlask(Flask):
    def __init__(self, *args, **kwargs):  # type: ignore
        super().__init__(*args, **kwargs)  # type: ignore
        self.game_sessions: GameSessionManager = GameSessionManager()


def create_app():
    load_dotenv()

    app = CustomFlask(__name__)

    init_endpoints(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)
    init_flask_jwt(jwt)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    db.init_app(app)
    create_tables(app, db)

    return app
