from app.cache.redis_client import redis
from app.cache.match_deletion_handler import handle_match_expiration  # pyright: ignore[reportUnknownVariableType]

pubsub = redis.pubsub()
pubsub.psubscribe(**{'__keyevent@0__:del': handle_match_expiration, '__keyevent@0__:expired': handle_match_expiration})
pubsub.run_in_thread(sleep_time=0.01)

redis.flushdb()  # pyright: ignore[reportUnknownMemberType]
