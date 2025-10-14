from typing import cast
from app.cache.cache_decorators import handle_cache_errors
from app.cache import redis
from app.error_handling.exceptions import CacheElementNotFoundException


SID_TIMEOUT = 86400


@handle_cache_errors
def save_user_session_to_cache(sid: str, user_id: int):
    redis.set(sid, user_id, SID_TIMEOUT)


@handle_cache_errors
def get_user_id_by_sid_from_cache(sid: str) -> int:
    user_id_bytes = cast(bytes | None, redis.get(sid))
    if not user_id_bytes:
        raise CacheElementNotFoundException()
    user_id = int(user_id_bytes)

    redis.expire(sid, SID_TIMEOUT)
    return user_id


@handle_cache_errors
def delete_user_session_from_cache(sid: str):
    redis.delete(sid)
