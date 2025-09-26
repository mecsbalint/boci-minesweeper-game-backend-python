from socketio import Server  # pyright: ignore[reportMissingTypeStubs]


def init_mp_game_events(sio: Server):

    @sio.event
    def create_game(sid, data):  # pyright: ignore[reportUnusedFunction]
        pass

    @sio.event
    def join_game(sid, data):  # pyright: ignore[reportUnusedFunction]
        pass

    @sio.event
    def rejoin_game(sid, data):  # pyright: ignore[reportUnusedFunction]
        pass

    @sio.event
    def make_player_step(sid, data):  # pyright: ignore[reportUnusedFunction]
        pass
        # sio.enter_room(sid, data["room"])
        # sio.emit("mp_game_event", data["msg"], room=data["room"])

    @sio.event
    def leave_game(sid, data):  # pyright: ignore[reportUnusedFunction]
        pass
