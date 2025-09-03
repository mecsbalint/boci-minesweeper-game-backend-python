from app.custom_flask import CustomFlask
from app.controllers import init_endpoints
from app.extensions import db, jwt
from app.database import init_db
from app.security.jwt import init_flask_jwt  # pyright: ignore[reportUnknownVariableType]


def create_app():

    app = CustomFlask(__name__)

    init_endpoints(app)

    init_flask_jwt(app, jwt)

    init_db(app, db)

    return app
