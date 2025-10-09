from typing import cast
from uuid import UUID
from app.cache import redis


def add_message_to_chat(match_id: UUID, message: tuple[str, str]):
    chat_key = _get_key_from_match_id(match_id)
    redis.rpush(chat_key, _create_str_from_message(message))


def get_chat_by_match_id_from_cache(match_id: UUID) -> list[tuple[str, str]]:
    chat_key = _get_key_from_match_id(match_id)
    messages: list[bytes] = cast(list[bytes], redis.lrange(chat_key, 0, -1))

    return [_create_message_from_str(msg.decode("utf-8")) for msg in messages]


def add_chat_to_cache(match_id: UUID):
    chat_key = _get_key_from_match_id(match_id)
    redis.rpush(chat_key, "__init__")
    redis.lpop(chat_key)


def remove_chat_from_cache(match_id: UUID):
    chat_key = _get_key_from_match_id(match_id)
    redis.delete(chat_key)


def _create_str_from_message(message: tuple[str, str]) -> str:
    return f"{message[0]}||{message[1]}"


def _create_message_from_str(string: str) -> tuple[str, str]:
    msg_list = string.split("||")
    return (msg_list[0], msg_list[1])


def _get_key_from_match_id(match_id: UUID) -> str:
    return f"chat_{match_id}"
