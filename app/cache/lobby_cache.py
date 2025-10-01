from typing import cast
from uuid import UUID
from app.cache.cache_decorators import handle_cache_errors
from app.cache import redis


LOBBY_KEY = "match_lobby"


@handle_cache_errors
def add_match_to_lobby(match_id: UUID):
    redis.sadd(LOBBY_KEY, str(match_id))


@handle_cache_errors
def remove_match_from_lobby(match_id: UUID):
    redis.srem(LOBBY_KEY, str(match_id))


@handle_cache_errors
def get_lobby() -> set[UUID]:
    ids = cast(set[bytes], redis.smembers(LOBBY_KEY))  # pyright: ignore[reportUnknownMemberType]
    return {UUID(item.decode("utf-8")) for item in ids}
