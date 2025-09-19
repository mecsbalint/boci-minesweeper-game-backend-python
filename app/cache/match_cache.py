from os import getenv
from typing import Literal, cast
from dotenv import load_dotenv
from app.cache import redis
import pickle
from app.cache.cache_decorators import handle_cache_errors
from app.error_handling.exceptions import CacheElementNotFoundException, CacheInvalidMatchException
from app.game.match import Match
from uuid import UUID, uuid4


SaveType = Literal["SP", "MP"]
KeyType = Literal["user", "match"]

load_dotenv()
REDIS_TIMEOUT = cast(int, getenv("REDIS_DEFAULT_TIMEOUT"))


@handle_cache_errors
def save_match_to_cache(match: Match, type: SaveType):
    user_keys = [_get_key(type, "user", participant.user_id) for participant in match.participants]

    match_id = match.id if match.id else uuid4()

    match_key = _get_key(type, "match", match_id)
    redis.set(match_key, pickle.dumps(match))

    for user_key in user_keys:
        redis.set(user_key, str(match_id))


@handle_cache_errors
def get_match_from_cache(user_id: int, type: SaveType) -> Match:
    user_key = _get_key("SP", "user", user_id)
    match_id_str = redis.get(user_key)

    if not isinstance(match_id_str, str):
        raise CacheElementNotFoundException()

    match_id = UUID(match_id_str)
    match_key = _get_key(type, "match", match_id)
    match = redis.get(match_key)

    if not isinstance(match, Match):
        raise CacheElementNotFoundException()
    else:
        return match


@handle_cache_errors
def remove_match_from_cache(match: Match, type: SaveType):
    if not match.id:
        raise CacheInvalidMatchException()

    match_key = _get_key(type, "match", match.id)
    redis.delete(match_key)

    user_keys = [_get_key(type, "user", participant.user_id) for participant in match.participants]
    for user_key in user_keys:
        redis.delete(user_key)


@handle_cache_errors
def check_match_in_cache(user_id: int, type: SaveType) -> bool:
    user_key = _get_key(type, "user", user_id)
    match_id_str = redis.get(user_key)

    if not isinstance(match_id_str, str):
        return False

    match_id = UUID(match_id_str)
    match_key = _get_key(type, "match", match_id)
    return redis.exists(match_key) == 1


def _get_key(type: SaveType, key_type: KeyType, id: int | UUID) -> str:
    return f"{type}_{key_type}_{id}"
