import logging
from typing import ParamSpec, TypeVar, Callable
from pydantic import ValidationError
from socketio import Server
from app.dto.exception_dto import ErrorDetailDto
from app.error_handling.exceptions import ApiException

logger = logging.getLogger(__name__)
R = TypeVar("R")
P = ParamSpec("P")


def websocket_error_handler(sio: Server):
    def websocket_error_handler_decorator(func: Callable[P, R]):
        def websocket_error_handler_wrapper(*args: P.args, **kwargs: P.kwargs):
            sid = args[0] if args else kwargs.get("sid", None)
            exception: Exception | None = None
            try:
                return func(*args, **kwargs)
            except ApiException as e:
                exception = e
                error_response = [error.model_dump() for error in e.errors]
            except ValidationError as e:
                exception = e
                error_response = [
                    ErrorDetailDto(code=f"VALIDATION_ERROR_{error['type']}", message=f"{'->'.join(map(str, error['loc']))}: {error['msg']}").model_dump()
                    for error in e.errors()
                    ]
            except Exception as e:
                exception = e
                e_details_dto = ErrorDetailDto(code="ERROR", message="An error occured during websocket communication")
                error_response = [e_details_dto.model_dump()]
            logger.error(
                f"WebSocket operation (session id: {sid}) failed in function {func.__name__}, error: {str(exception)}"
                )
            sio.emit("error",  error_response, to=sid)

        return websocket_error_handler_wrapper
    return websocket_error_handler_decorator
