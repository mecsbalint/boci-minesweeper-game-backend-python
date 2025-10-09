from typing import cast
from uuid import UUID
from app.cache.chat_cache import add_message_to_chat, get_chat_by_match_id_from_cache
from app.cache.match_cache import get_match_by_user_id_from_cache
from app.error_handling.exceptions import UserNotFoundException
from app.service.user_service import get_user_by_id


def add_message(user_id: int, message: str) -> tuple[UUID, list[tuple[str, str]]]:
    match_id = cast(UUID, get_match_by_user_id_from_cache(user_id, "MP").id)
    user = get_user_by_id(user_id)

    if not user:
        raise UserNotFoundException("id")

    chat = add_message_to_chat(match_id, (user.name, message))

    return (match_id, chat)


def get_chat_by_user_id(user_id: int) -> list[tuple[str, str]]:
    match_id = cast(UUID, get_match_by_user_id_from_cache(user_id, "MP").id)

    return get_chat_by_match_id_from_cache(match_id)
