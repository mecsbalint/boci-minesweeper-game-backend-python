from typing import Any
from socketio import Server  # pyright: ignore[reportMissingTypeStubs]
from app.cache.websocket_cache import save_user_session_to_cache, delete_user_session_from_cache
from app.dto.user_dto import WSAuthDto
from app.event_handlers.game_lobby_events import init_game_lobby_events
from app.security.jwt_handling import decode_jwt_token
from app.event_handlers.mp_game_events import init_mp_game_events  # pyright: ignore[reportMissingTypeStubs]


def init_websocket_events(sio: Server):
    @sio.event
    def connect(sid: str, environ, auth: dict[Any, Any]):
        auth_dto = WSAuthDto(**auth)
        user_id = decode_jwt_token(auth_dto.jwt)
        save_user_session_to_cache(sid, user_id)
        print('connect ', sid)

    @sio.event
    def disconnect(sid: str):
        delete_user_session_from_cache(sid)
        print('disconnect ', sid)

    init_mp_game_events(sio)
    init_game_lobby_events(sio)
