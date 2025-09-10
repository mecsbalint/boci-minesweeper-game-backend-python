from flask import Flask
from app.error_handling.error_handlers import init_error_handlers


def init_error_handling(app: Flask):
    init_error_handlers(app)
