from uuid import UUID
from app.database.db_models import User
from app.dto.chat_dto import ChatDto


def add_message(user_id: int, message: tuple[str, str]) -> tuple[UUID, ChatDto]:
    pass


def get_chat_dto_by_user_id(user_id: int) -> ChatDto:
    pass


def add_user_to_chat(match_id: UUID, user: User):
    pass


def remove_user_from_chat(user: User):
    pass
