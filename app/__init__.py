from flask import Flask
from app.controllers import init_endpoints
from app.database import init_db
from app.error_handling import init_error_handling
from app.security import init_security
import socketio  # pyright: ignore[reportMissingTypeStubs]
from app.extensions import sio


def create_app():

    flask_app = Flask(__name__)

    init_endpoints(flask_app)

    init_security(flask_app)

    init_db(flask_app)

    init_error_handling(flask_app)

    app = socketio.WSGIApp(sio, flask_app)

    return app
