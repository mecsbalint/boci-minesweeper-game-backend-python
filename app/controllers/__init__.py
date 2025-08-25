from .user_controllers import init_user_endpoints
from .game_controllers import init_game_endpoints


def init_endpoints(app):
    init_user_endpoints(app)
    init_game_endpoints(app)
