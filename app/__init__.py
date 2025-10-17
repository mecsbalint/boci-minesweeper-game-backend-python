import os
from typing import cast
from dotenv import load_dotenv
from flask import Flask
from app.controllers import init_endpoints
from app.database import init_db
from app.error_handling.flask_error_handlers import init_error_handlers
from app.security import init_security
import socketio  # pyright: ignore[reportMissingTypeStubs]
from app.event_handlers import init_websocket_events

load_dotenv()
FRONTEND_URI = str(os.getenv("FRONTEND_URI"))
PORT = int(cast(str, os.getenv("PORT")))

flask_app = Flask(__name__)
sio = socketio.Server(async_mode="gevent", cors_allowed_origins=[FRONTEND_URI, f"http://localhost:{PORT}"])


def create_app():

    init_endpoints(flask_app, sio)

    init_websocket_events(sio)

    init_security(flask_app)

    init_db(flask_app)

    init_error_handlers(flask_app)

    app = socketio.WSGIApp(sio, flask_app)

    return app
