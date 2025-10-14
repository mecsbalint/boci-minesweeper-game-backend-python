import logging
from dotenv import load_dotenv
from os import getenv
from typing import cast
from redis import from_url
from app.cache.match_deletion_handler import handle_match_expiration  # pyright: ignore[reportUnknownVariableType]

logger = logging.getLogger(__name__)
load_dotenv()

REDIS_TIMEOUT = cast(int, getenv("REDIS_DEFAULT_TIMEOUT"))

redis_url = cast(str, getenv("REDIS_URL"))
redis = from_url(redis_url)
redis.config_set("notify-keyspace-events", "Exg")

pubsub = redis.pubsub()
pubsub.psubscribe(**{'__keyevent@0__:del': handle_match_expiration, '__keyevent@0__:expired': handle_match_expiration})
pubsub.run_in_thread(sleep_time=0.01)

redis.flushdb()  # pyright: ignore[reportUnknownMemberType]
