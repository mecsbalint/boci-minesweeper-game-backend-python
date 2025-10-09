from socketio import Server  # pyright: ignore[reportMissingTypeStubs]
from app.cache.websocket_cache import get_user_id_by_sid_from_cache
from app.error_handling.exceptions import InvalidChatMessageException
from app.error_handling.websocket_error_handler_decorator import websocket_error_handler  # pyright: ignore[reportMissingTypeStubs]
from app.service import chat_service


def init_chat_events(sio: Server):

    @sio.event
    @websocket_error_handler(sio)
    def add_message(sid: str, data: list[str]):  # pyright: ignore[reportUnusedFunction]
        message = tuple(data)
        if len(message) != 2:
            raise InvalidChatMessageException()

        user_id = get_user_id_by_sid_from_cache(sid)

        match_id, chat = chat_service.add_message(user_id, message)

        sio.emit(chat.model_dump(by_alias=True), room=match_id)
