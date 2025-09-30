from flask import Flask
from app.controllers import init_endpoints
from app.database import init_db
from app.error_handling import init_error_handling
from app.security import init_security
import socketio  # pyright: ignore[reportMissingTypeStubs]
from app.event_handlers import init_websocket_events

flask_app = Flask(__name__)


def create_app():

    sio = socketio.Server(cors_allowed_origins="http://localhost:5173")

    init_endpoints(flask_app, sio)

    init_websocket_events(sio)

    init_security(flask_app)

    init_db(flask_app)

    init_error_handling(flask_app)

    app = socketio.WSGIApp(sio, flask_app)

    return app
