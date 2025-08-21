from flask import Flask
from app import routes
from app.extensions import db
from app import models
from dotenv import load_dotenv
import os


def create_app():
    load_dotenv()

    app = Flask(__name__)

    routes.init_endpoints(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    db.init_app(app)
    models.init_models(db)

    return app
