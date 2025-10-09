from uuid import UUID
from app.dto.chat_dto import ChatDto


def add_message(user_id: int, message: tuple[str, str]) -> tuple[UUID, ChatDto]:
    pass


def get_chat_dto_by_user_id(user_id: int) -> ChatDto:
    pass
