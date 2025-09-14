import logging
from dotenv import load_dotenv
from app.error_handling.exceptions import CacheConnectionException, CacheOperationException
from app.extensions import cache
from flask import Flask
from os import getenv
from typing import Callable, cast, Any, TypeVar
from redis.exceptions import ConnectionError, TimeoutError, ResponseError, InvalidResponse
from pickle import PickleError, UnpicklingError

logger = logging.getLogger(__name__)


def init_cache(app: Flask):
    load_dotenv()

    redis_url = cast(str, getenv("REDIS_URL"))
    cache_default_timeout = int(cast(str, getenv("CACHE_DEFAULT_TIMEOUT")))

    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_URL"] = redis_url
    app.config["CACHE_DEFAULT_TIMEOUT"] = cache_default_timeout

    cache.init_app(app)  # pyright: ignore[reportUnknownMemberType]


R = TypeVar("R")


def handle_cache_errors(func: Callable[..., R]) -> Callable[..., R]:

    def handle_cache_errors_wrapper(*args: Any, **kwargs: Any) -> R:
        try:
            return func(*args, **kwargs)
        except (ConnectionError, TimeoutError, ResponseError, InvalidResponse, TypeError, PickleError, UnpicklingError, ValueError) as e:
            logger.error(f"Cache operation failed in function {func.__name__} with args={args}, kwargs={kwargs}: {str(e)}")
            logger.debug("Full traceback:", exc_info=True)

            if isinstance(e, (ConnectionError, TimeoutError, ResponseError, InvalidResponse)):
                raise CacheConnectionException()
            else:
                raise CacheOperationException()

    return handle_cache_errors_wrapper
