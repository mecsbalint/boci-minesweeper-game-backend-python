from socketio import Server
from app.cache.match_cache import get_matches_by_ids_from_cache
from app.cache.lobby_cache import get_lobby
from app.dto.game_dto import MatchLobbyDto


LOBBY_ROOM = "lobby"


def init_game_lobby_events(sio: Server):

    @sio.event
    def join_lobby(sid: str):  # pyright: ignore[reportUnusedFunction]
        match_lobby_dtos = _create_match_lobby_dtos()

        sio.enter_room(sid, LOBBY_ROOM)
        sio.emit("get_lobby", match_lobby_dtos, to=sid)


def broadcast_lobby_update(sio: Server):
    match_lobby_dtos = _create_match_lobby_dtos()

    sio.emit("lobby_update", match_lobby_dtos, room=LOBBY_ROOM)


def _create_match_lobby_dtos() -> list[MatchLobbyDto]:
    match_ids = get_lobby()
    match_set = get_matches_by_ids_from_cache(match_ids, "MP")

    return [MatchLobbyDto.from_match(match) for match in match_set]
