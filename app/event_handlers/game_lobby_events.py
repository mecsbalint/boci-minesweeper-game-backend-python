from typing import Any
from socketio import Server
from app.cache.match_cache import get_matches_by_ids_from_cache
from app.cache.lobby_cache import get_lobby
from app.dto.game_dto import MatchLobbyDto


LOBBY_ROOM = "lobby"


def init_game_lobby_events(sio: Server):

    @sio.event
    def join_lobby(sid: str):  # pyright: ignore[reportUnusedFunction]
        print("JOIN LOBBY +++++++++++++++++++++++++++++++++++")
        match_lobby_dto_dicts = _create_match_lobby_dto_dicts()

        sio.enter_room(sid, LOBBY_ROOM)
        sio.emit("lobby_update", match_lobby_dto_dicts, to=sid)


def broadcast_lobby_update(sio: Server):
    print("BROADCAST LOBBY +++++++++++++++++++++++++++++++++++")
    match_lobby_dto_dicts = _create_match_lobby_dto_dicts()

    sio.emit("lobby_update", match_lobby_dto_dicts, room=LOBBY_ROOM)


def _create_match_lobby_dto_dicts() -> list[dict[str, Any]]:
    match_ids = get_lobby()
    match_set = get_matches_by_ids_from_cache(match_ids, "MP")

    return [MatchLobbyDto.from_match(match).model_dump(by_alias=True) for match in match_set]
