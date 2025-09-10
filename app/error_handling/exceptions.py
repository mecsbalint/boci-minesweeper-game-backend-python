
from app.dto.exception_dto import ExceptionDto


class ApiException(Exception):
    def __init__(self, status: int, *errors: ExceptionDto) -> None:
        super().__init__()
        self._status = status
        self._errors = errors

    @property
    def errors(self):
        return self._errors

    @property
    def status(self):
        return self._status


class CacheException(ApiException):
    def __init__(self, *errors: ExceptionDto) -> None:
        super().__init__(500, *errors)


class CacheOperationException(CacheException):
    def __init__(self) -> None:
        error = ExceptionDto(
            code="CACHE_OPERATION_ERROR",
            message="An error occured during cache operation")
        super().__init__(error)


class CacheConnectionException(CacheException):
    def __init__(self) -> None:
        error = ExceptionDto(
            code="CACHE_CONNECTION_ERROR",
            message="Cache service is currently unavailable")
        super().__init__(error)


class GameException(ApiException):
    def __init__(self, status: int, *errors: ExceptionDto) -> None:
        super().__init__(status, *errors)


class InvalidMapException(GameException):
    def __init__(self) -> None:
        error = ExceptionDto(
            code="GAME_MAP_ERROR",
            message="An error occured during map generation or initialization")
        super().__init__(500, error)


class GameNotFoundException(GameException):
    def __init__(self) -> None:
        error = ExceptionDto(
            code="GAME_NOT_FOUND",
            message="There is no game of the user")
        super().__init__(404, error)


class UserException(ApiException):
    pass


class InvalidPasswordException(UserException):
    def __init__(self) -> None:
        error = ExceptionDto(
            code="USER_INVALID_PASSWORD",
            message="The password is incorrect")
        super().__init__(401, error)


class UserNotFoundException(UserException):
    def __init__(self, identifier_type: str) -> None:
        error = ExceptionDto(
            code="USER_NOT_FOUND",
            message=f"There is no user registered with the provided {identifier_type}")
        super().__init__(404, error)


class UserAlreadyExistException(UserException):
    def __init__(self) -> None:
        error = ExceptionDto(
            code="USER_EXIST",
            message="A user has been already registered with this e-mail address")
        super().__init__(409, error)
