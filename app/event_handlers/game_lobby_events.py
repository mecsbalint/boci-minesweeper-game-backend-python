from socketio import Server
from app.error_handling.websocket_error_handler_decorator import websocket_error_handler
from app.service.lobby_service import create_match_lobby_dto_dicts


LOBBY_ROOM = "lobby"


def init_game_lobby_events(sio: Server):

    @sio.event
    @websocket_error_handler(sio)
    def join_lobby(sid: str):  # pyright: ignore[reportUnusedFunction]
        match_lobby_dto_dicts = create_match_lobby_dto_dicts()

        sio.enter_room(sid, LOBBY_ROOM)
        sio.emit("lobby_update", match_lobby_dto_dicts, to=sid)


def broadcast_lobby_update(sio: Server):
    match_lobby_dto_dicts = create_match_lobby_dto_dicts()

    sio.emit("lobby_update", match_lobby_dto_dicts, room=LOBBY_ROOM)
