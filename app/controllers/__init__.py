from .user_controllers import init_user_endpoints


def init_endpoints(app):
    init_user_endpoints(app)
