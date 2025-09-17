from flask import Flask
from .user_controllers import init_user_endpoints
from .sp_game_controllers import init_game_endpoints


def init_endpoints(app: Flask):
    init_user_endpoints(app)
    init_game_endpoints(app)
