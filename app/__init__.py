from flask import Flask
from app import routes


def create_app():
    app = Flask(__name__)

    routes.init_endpoints(app)

    return app
