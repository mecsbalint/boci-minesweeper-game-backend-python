from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import socketio  # pyright: ignore[reportMissingTypeStubs]

db = SQLAlchemy()

jwt = JWTManager()

sio = socketio.Server()
