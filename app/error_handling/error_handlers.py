from flask import Flask, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException
from app.error_handling.exceptions import ApiException


def init_error_handlers(app: Flask):

    @app.errorhandler(ValidationError)
    def handle_validation_error(exception: ValidationError):  # pyright: ignore[reportUnusedFunction]
        errors = exception.errors()
        error_logs: list[dict[str, str]] = []
        for error in errors:
            error_logs.append({
                "code": error["type"],
                "message": f"{"->".join(map(str, error["loc"]))}: {error["msg"]}"
            })
        return jsonify(error_logs), 400

    @app.errorhandler(ApiException)
    def handle_app_exception(exception: ApiException):  # pyright: ignore[reportUnusedFunction]
        return jsonify(exception.errors), exception.status

    app.register_error_handler(HTTPException, http_exception_handler)


def http_exception_handler(exception: HTTPException):
    response_code = exception.code if exception.code else 500
    description = exception.description if exception.description else "Internal Server Error"
    return jsonify([{"code": f"HTTP_{type(exception).__name__}", "message": description}]), response_code
