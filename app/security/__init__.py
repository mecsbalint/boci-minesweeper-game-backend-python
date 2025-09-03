from app.custom_flask import CustomFlask
from app.security.jwt import init_flask_jwt


def init_security(app: CustomFlask):
    init_flask_jwt(app)
