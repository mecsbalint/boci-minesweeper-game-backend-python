from typing import Literal, cast
from app.cache import REDIS_TIMEOUT, redis
import pickle
from app.cache.cache_decorators import handle_cache_errors
from app.error_handling.exceptions import (CacheElementNotFoundException,
                                           CacheInvalidMatchException,
                                           CacheConcurrencyException)
from app.game.match import Match
from uuid import UUID, uuid4


SaveType = Literal["SP", "MP"]
KeyType = Literal["user", "match"]


@handle_cache_errors
def save_match_to_cache(match: Match, type: SaveType) -> Match:
    user_keys = [_get_key(type, "user", participant.user_id) for participant in match.participants]

    match.id = match.id if match.id else uuid4()

    match_key = _get_key(type, "match", match.id)

    with redis.pipeline() as pipeline:  # pyright: ignore[reportUnknownMemberType]
        pipeline.watch(match_key, *user_keys)

        current_bytes = cast(bytes | None, redis.get(match_key))
        current_match: Match | None = pickle.loads(current_bytes) if current_bytes is not None else None
        if current_match and match.version != current_match.version:
            raise CacheConcurrencyException()

        pipeline.multi()
        match.version += 1
        pipeline.set(match_key, pickle.dumps(match), ex=REDIS_TIMEOUT)
        for user_key in user_keys:
            pipeline.set(user_key, str(match.id), ex=REDIS_TIMEOUT)
        pipeline.execute()

        return match


@handle_cache_errors
def get_match_by_user_id_from_cache(user_id: int, type: SaveType) -> Match:
    user_key = _get_key(type, "user", user_id)

    match_id_bytes = cast(bytes | None, redis.get(user_key))
    if not match_id_bytes:
        raise CacheElementNotFoundException()
    match_id_str = match_id_bytes.decode("utf-8")

    match_id = UUID(match_id_str)

    return get_match_by_id_from_cache(match_id, type)


@handle_cache_errors
def get_match_by_id_from_cache(match_id: UUID, type: SaveType) -> Match:
    match_key = _get_key(type, "match", match_id)
    match_bytes = cast(bytes | None, redis.get(match_key))
    match_obj: Match | None = pickle.loads(match_bytes) if match_bytes is not None else None

    if not isinstance(match_obj, Match):
        raise CacheElementNotFoundException()
    else:
        return match_obj


@handle_cache_errors
def get_matches_by_ids_from_cache(match_ids: set[UUID], type: SaveType):
    match_set: set[Match] = set()

    for id in match_ids:
        match = get_match_by_id_from_cache(id, type)
        match_set.add(match)

    return match_set


@handle_cache_errors
def remove_match_from_cache(match: Match, type: SaveType):
    if not match.id:
        raise CacheInvalidMatchException()

    match_key = _get_key(type, "match", match.id)
    user_keys = [_get_key(type, "user", participant.user_id) for participant in match.participants]

    with redis.pipeline() as pipeline:  # pyright: ignore[reportUnknownMemberType]
        pipeline.watch(match_key, *user_keys)

        current_bytes = cast(bytes | None, redis.get(match_key))
        current_match: Match | None = pickle.loads(current_bytes) if current_bytes is not None else None
        if current_match and match.version != current_match.version:
            raise CacheConcurrencyException()

        pipeline.multi()
        pipeline.delete(match_key)
        for user_key in user_keys:
            pipeline.delete(user_key)
        pipeline.execute()


@handle_cache_errors
def check_match_in_cache(user_id: int, type: SaveType) -> bool:
    user_key = _get_key(type, "user", user_id)

    match_id_bytes = cast(bytes | None, redis.get(user_key))
    if not match_id_bytes:
        return False
    match_id_str = match_id_bytes.decode("utf-8")

    match_id = UUID(match_id_str)
    match_key = _get_key(type, "match", match_id)
    return redis.exists(match_key) == 1


def _get_key(type: SaveType, key_type: KeyType, id: int | UUID) -> str:
    return f"{type}_{key_type}_{id}"
