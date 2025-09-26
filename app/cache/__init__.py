import logging
from dotenv import load_dotenv
from os import getenv
from typing import cast
from redis import from_url  # pyright: ignore[reportUnknownVariableType]

logger = logging.getLogger(__name__)
load_dotenv()

REDIS_TIMEOUT = cast(int, getenv("REDIS_DEFAULT_TIMEOUT"))

redis_url = cast(str, getenv("REDIS_URL"))
redis = from_url(redis_url)
redis.flushdb()  # pyright: ignore[reportUnknownMemberType]
