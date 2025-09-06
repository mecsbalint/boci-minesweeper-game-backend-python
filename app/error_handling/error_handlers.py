from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from app.error_handling.exceptions import ApiException


def init_error_handlers(app: Flask):

    @app.errorhandler(ApiException)
    def handle_app_exception(error: ApiException):  # pyright: ignore[reportUnusedFunction]
        return jsonify(error.to_dict()), error.status

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):  # pyright: ignore[reportUnusedFunction]
        response_code = error.code if error.code else 500
        description = error.description if error.description else "Internal Server Error"
        return jsonify({"code": f"HTTP_{type(error).__name__}", "message": description}), response_code
