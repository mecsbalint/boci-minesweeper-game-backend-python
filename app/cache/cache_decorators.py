import logging
from app.error_handling.exceptions import CacheConcurrencyException, CacheConnectionException, CacheOperationException
from typing import Callable, ParamSpec, TypeVar
from redis.exceptions import ConnectionError, TimeoutError, ResponseError, InvalidResponse, WatchError
from pickle import PickleError, UnpicklingError


logger = logging.getLogger(__name__)
R = TypeVar("R")
P = ParamSpec("P")


def handle_cache_errors(func: Callable[P, R]) -> Callable[P, R]:

    def handle_cache_errors_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return func(*args, **kwargs)
        except (ConnectionError, TimeoutError, ResponseError, InvalidResponse, TypeError, PickleError, UnpicklingError, ValueError, WatchError) as e:
            logger.error(f"Cache operation failed in function {func.__name__} with args={args}, kwargs={kwargs}: {str(e)}")
            logger.debug("Full traceback:", exc_info=True)

            if isinstance(e, (ConnectionError, TimeoutError, ResponseError, InvalidResponse)):
                raise CacheConnectionException()
            elif isinstance(e, WatchError):
                raise CacheConcurrencyException()
            else:
                raise CacheOperationException()

    return handle_cache_errors_wrapper
