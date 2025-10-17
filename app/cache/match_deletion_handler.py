import pickle
from typing import Any, cast
from uuid import UUID
from app.cache.cache_decorators import handle_cache_errors
from app.cache.chat_cache import set_ttl_for_chat
from app.cache.lobby_cache import get_lobby, remove_match_from_lobby
from app.cache.match_cache import get_key, get_match_key_from_match_exp_key, get_type_from_match_key
from app.cache.redis_client import REDIS_TIMEOUT, redis
from app.event_handlers.game_lobby_events import broadcast_lobby_update
from app.game.match import Match


def handle_match_deletion(match_exp_key: str):
    from app import sio
    match_key = get_match_key_from_match_exp_key(match_exp_key)
    match_type = get_type_from_match_key(match_key)

    match_bytes = cast(bytes | None, redis.get(match_key))
    match: Match | None = pickle.loads(match_bytes) if match_bytes else None

    if not isinstance(match, Match):
        return

    user_keys = [get_key(match_type, "user", participant.user_id) for participant in match.participants]
    valid_user_keys: list[str] = []

    for user_key in user_keys:
        match_id_bytes = cast(bytes | None, redis.get(user_key))
        match_id_str = match_id_bytes.decode("utf-8") if match_id_bytes else None
        if match_id_str and match_id_str == str(match.id):
            valid_user_keys.append(user_key)

    with redis.pipeline() as pipeline:  # pyright: ignore[reportUnknownMemberType]
        pipeline.watch(match_key, *valid_user_keys)

        pipeline.multi()
        pipeline.delete(match_key)
        if match_type == "MP":
            set_ttl_for_chat(cast(UUID, match.id))
        for user_key in valid_user_keys:
            pipeline.delete(user_key)
        if not pipeline.execute():
            redis.set(match_exp_key, match_key, ex=REDIS_TIMEOUT)
        elif match.id in get_lobby():
            remove_match_from_lobby(cast(UUID, match.id))
            broadcast_lobby_update(sio)


@handle_cache_errors
def handle_key_expiration_deletion(message: dict[str, Any]):
    match_exp_key = cast(bytes, message["data"]).decode("utf-8")
    if "match_exp" not in match_exp_key:
        return
    handle_match_deletion(match_exp_key)
