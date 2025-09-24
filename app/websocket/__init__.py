from socketio import Server

from app.websocket.mp_game_events import init_mp_game_events  # pyright: ignore[reportMissingTypeStubs]


def init_websocket_events(sio: Server):
    @sio.event
    def connect(sid, environ):
        print('connect ', sid)

    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)

    init_mp_game_events(sio)
