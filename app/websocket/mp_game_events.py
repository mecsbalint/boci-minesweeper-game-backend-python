from socketio import Server  # pyright: ignore[reportMissingTypeStubs]


def init_mp_game_events(sio: Server):

    @sio.event
    def mp_game_event(sid, data):
        print('message ', data)
        sio.emit("mp_game_event", data)
