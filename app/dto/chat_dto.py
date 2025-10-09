from app.dto.dto_base_model import DtoBaseModel
from app.game.chat_model import Chat


class ChatDto(DtoBaseModel):
    messages: list[tuple[str, str]]

    @classmethod
    def from_chat(cls, chat: Chat):
        return cls(messages=chat.messages)
