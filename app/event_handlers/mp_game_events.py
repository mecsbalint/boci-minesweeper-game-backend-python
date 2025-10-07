from typing import Any, cast
from uuid import UUID
from socketio import Server
from app.cache.match_cache import get_match_by_user_id_from_cache
from app.cache.websocket_cache import get_user_id_by_sid_from_cache
from app.dto.game_dto import MatchDto, MatchDtoDict, MatchIdDto, PlayerMoveDto  # pyright: ignore[reportMissingTypeStubs]
from app.error_handling.exceptions import CacheConcurrencyException, CacheElementNotFoundException
from app.error_handling.websocket_error_handler_decorator import websocket_error_handler
from app.service import game_service


def init_mp_game_events(sio: Server):

    @sio.event
    @websocket_error_handler(sio)
    def join_game(sid: str, data: dict[Any, Any]):  # pyright: ignore[reportUnusedFunction]
        user_id = get_user_id_by_sid_from_cache(sid)
        match_id = MatchIdDto(**data).id
        match_dtos_dict: MatchDtoDict = game_service.add_user_to_match(user_id, match_id, "MP", sio)

        sio.enter_room(sid, match_id)

        _emit_to_participants(sio, match_id, match_dtos_dict)

    @sio.event
    @websocket_error_handler(sio)
    def rejoin_game(sid: str):  # pyright: ignore[reportUnusedFunction]
        user_id = get_user_id_by_sid_from_cache(sid)
        match_dto: MatchDto = game_service.get_active_game(user_id, "MP")

        sio.enter_room(sid, cast(UUID, match_dto.id))
        sio.emit("current_game_state", match_dto.model_dump(by_alias=True), to=sid)

    @sio.event
    @websocket_error_handler(sio)
    def make_player_move(sid: str, data: dict[Any, Any]):  # pyright: ignore[reportUnusedFunction]
        user_id = get_user_id_by_sid_from_cache(sid)
        player_move = PlayerMoveDto(**data)
        match_dtos_dict: MatchDtoDict = game_service.make_player_move(user_id, player_move, "MP")
        match_id = cast(str, match_dtos_dict[user_id].id)

        _emit_to_participants(sio, match_id, match_dtos_dict)

    @sio.event
    @websocket_error_handler(sio)
    def leave_game(sid: str):  # pyright: ignore[reportUnusedFunction]
        user_id = get_user_id_by_sid_from_cache(sid)
        match_id = cast(UUID, get_match_by_user_id_from_cache(user_id, "MP").id)
        sio.leave_room(sid, match_id)


def _emit_to_participants(sio: Server, match_id: str, match_dtos_dict: MatchDtoDict):
    participant_sids_raw = cast(set[Any], sio.manager.get_participants("/", match_id))
    print("participants:", participant_sids_raw)
    for item in participant_sids_raw:
        try:
            participant_sid = cast(str, item if not isinstance(item, tuple) else item[0])
            participant_id = get_user_id_by_sid_from_cache(participant_sid)
            match_dto = match_dtos_dict.get(participant_id)
            if match_dto:
                sio.emit("current_game_state", match_dto.model_dump(by_alias=True), to=participant_sid)
        except CacheElementNotFoundException:
            continue
