from dotenv import load_dotenv
from app.extensions import cache
from flask import Flask
from os import getenv
from typing import cast


def init_cache(app: Flask):
    load_dotenv()

    redis_host = cast(str, getenv("REDIS_HOST"))
    redis_port = int(cast(int, getenv("REDIS_PORT")))
    redis_db = int(cast(str, getenv("REDIS_DB")))
    cache_default_timeout = int(cast(str, getenv("CACHE_DEFAULT_TIMEOUT")))

    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_HOST"] = redis_host
    app.config["CACHE_REDIS_PORT"] = redis_port
    app.config["CACHE_REDIS_DB"] = redis_db
    app.config["CACHE_DEFAULT_TIMEOUT"] = cache_default_timeout

    cache.init_app(app)  # pyright: ignore[reportUnknownMemberType]
