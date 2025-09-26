import os
from dotenv import load_dotenv
from flask import Flask
from app.security.flask_jwt_extended_config import init_flask_jwt


load_dotenv()
JWT_SECRET_KEY = str(os.getenv("JWT_SECRET_KEY"))


def init_security(app: Flask):
    init_flask_jwt(app)
