from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def init_error_handlers(app: Flask):

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):  # pyright: ignore[reportUnusedFunction]
        response_code = e.code if e.code else 400
        return jsonify({"error": e.description}), response_code
