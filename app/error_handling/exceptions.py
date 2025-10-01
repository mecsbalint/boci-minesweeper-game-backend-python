
from app.dto.exception_dto import ErrorDetailDto


class ApiException(Exception):
    def __init__(self, status: int, *errors: ErrorDetailDto) -> None:
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
    def __init__(self, status: int, *errors: ErrorDetailDto) -> None:
        super().__init__(status, *errors)


class CacheOperationException(CacheException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="CACHE_OPERATION_ERROR",
            message="An error occured during cache operation")
        super().__init__(500, error)


class CacheConnectionException(CacheException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="CACHE_CONNECTION_ERROR",
            message="Cache service is currently unavailable")
        super().__init__(500, error)


class CacheElementNotFoundException(CacheException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="CACHE_ELEMENT_NOT_FOUND_ERROR",
            message="The element is not found in cache")
        super().__init__(404, error)


class CacheInvalidMatchException(CacheException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="CACHE_INVALID_MATCH_ERROR",
            message="The match the cache tried to use is invalid")
        super().__init__(404, error)


class CacheConcurrencyException(CacheException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="CACHE_CONCURRENCY_ERROR",
            message="Version conflict: the game state has advanced")
        super().__init__(409, error)


class GameException(ApiException):
    def __init__(self, status: int, *errors: ErrorDetailDto) -> None:
        super().__init__(status, *errors)


class InvalidBoardException(GameException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="GAME_BOARD_ERROR",
            message="An error occured during map generation or initialization")
        super().__init__(500, error)


class InvalidMapException(GameException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="GAME_MAP_ERROR",
            message="Cannot set winner before the game is finished.")
        super().__init__(500, error)


class InvalidCellException(GameException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="GAME_CELL_ERROR",
            message="An error occured during creation or modification of a cell")
        super().__init__(500, error)


class InvalidPlayerMoveException(GameException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="GAME_INVALID_PLAYER_MOVE",
            message="The player's move can't be made in the current game")
        super().__init__(400, error)


class GameNotFoundException(GameException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="GAME_NOT_FOUND",
            message="There is no game of the user")
        super().__init__(404, error)


class GameIsFullException(GameException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="GAME_IS_FULL",
            message="There is no free slots in the game the user tries to join")
        super().__init__(400, error)


class InvalidGameStateException(GameException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="INVALID_GAME_STATE",
            message="The game is in a state when it can't accept player moves")
        super().__init__(400, error)


class UserException(ApiException):
    pass


class InvalidPasswordException(UserException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="USER_INVALID_PASSWORD",
            message="The password is incorrect")
        super().__init__(401, error)


class UserNotFoundException(UserException):
    def __init__(self, identifier_type: str) -> None:
        error = ErrorDetailDto(
            code="USER_NOT_FOUND",
            message=f"There is no user registered with the provided {identifier_type}")
        super().__init__(404, error)


class UserAlreadyExistException(UserException):
    def __init__(self) -> None:
        error = ErrorDetailDto(
            code="USER_EXIST",
            message="A user has been already registered with this e-mail address")
        super().__init__(409, error)
