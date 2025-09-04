from flask import Flask
from app.security.jwt import init_flask_jwt


def init_security(app: Flask):
    init_flask_jwt(app)
