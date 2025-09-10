from flask import Flask
from app.cache import init_cache
from app.controllers import init_endpoints
from app.database import init_db
from app.error_handling import init_error_handling
from app.security import init_security


def create_app():

    app = Flask(__name__)

    init_endpoints(app)

    init_security(app)

    init_db(app)

    init_cache(app)

    init_error_handling(app)

    return app
