from flask import Flask, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException
from app.dto.exception_dto import ExceptionDto
from app.error_handling.exceptions import ApiException
from sqlalchemy.exc import OperationalError, InterfaceError, InternalError, IntegrityError, DataError, ProgrammingError, SQLAlchemyError


def init_error_handlers(app: Flask):

    @app.errorhandler(OperationalError)
    @app.errorhandler(InterfaceError)
    @app.errorhandler(InternalError)
    def handle_database_connection_error(exception: OperationalError | InterfaceError):  # pyright: ignore[reportUnusedFunction]
        return jsonify([ExceptionDto(code="DATABASE_CONNECTION_FAILED", message=str(exception.__cause__)).model_dump()]), 500

    @app.errorhandler(IntegrityError)
    @app.errorhandler(DataError)
    @app.errorhandler(ProgrammingError)
    def handle_database_query_error(exception: IntegrityError | DataError | ProgrammingError):  # pyright: ignore[reportUnusedFunction]
        return jsonify([ExceptionDto(code="DATABASE_QUERY_FAILED", message=str(exception.__cause__)).model_dump()]), 500

    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(exception: SQLAlchemyError):  # pyright: ignore[reportUnusedFunction]
        return jsonify([ExceptionDto(code="DATABASE_ERROR", message=str(exception.__cause__)).model_dump()]), 500

    @app.errorhandler(ValidationError)
    def handle_validation_error(exception: ValidationError):  # pyright: ignore[reportUnusedFunction]
        errors = exception.errors()
        error_logs: list[ExceptionDto] = []
        for error in errors:
            error_logs.append(ExceptionDto(
                code=f"VALIDATION_ERROR_{error["type"]}",
                message=f"{"->".join(map(str, error["loc"]))}: {error["msg"]}"))
        return jsonify([error.model_dump() for error in error_logs]), 400

    @app.errorhandler(ApiException)
    def handle_app_exception(exception: ApiException):  # pyright: ignore[reportUnusedFunction]
        return jsonify([error.model_dump() for error in exception.errors]), exception.status

    app.register_error_handler(HTTPException, http_exception_handler)


def http_exception_handler(exception: HTTPException):
    response_code = exception.code if exception.code else 500
    description = exception.description if exception.description else "Internal Server Error"
    return (
        jsonify([ExceptionDto(code=f"HTTP_{type(exception).__name__}", message=description).model_dump()]),
        response_code
        )
