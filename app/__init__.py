from app.cache import init_cache
from app.custom_flask import CustomFlask
from app.controllers import init_endpoints
from app.database import init_db
from app.security import init_security


def create_app():

    app = CustomFlask(__name__)

    init_endpoints(app)

    init_security(app)

    init_db(app)

    init_cache(app)

    return app
