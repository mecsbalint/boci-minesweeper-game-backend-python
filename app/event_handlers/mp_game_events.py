from typing import Any, cast
from uuid import UUID
from socketio import Server
from app.cache.match_cache import get_match_by_user_id_from_cache
from app.cache.websocket_cache import get_user_id_by_sid_from_cache
from app.dto.game_dto import MatchDto, MatchIdDto, PlayerMoveDto  # pyright: ignore[reportMissingTypeStubs]
from app.event_handlers.with_app_context import with_app_context
from app.service import game_service


def init_mp_game_events(sio: Server):

    @sio.event
    @with_app_context
    def join_game(sid: str, data: dict[Any, Any]):  # pyright: ignore[reportUnusedFunction]
        user_id = get_user_id_by_sid_from_cache(sid)
        match_id = MatchIdDto(**data).id
        match_dto: MatchDto = game_service.add_user_to_match(user_id, match_id, "MP", sio)

        sio.enter_room(sid, match_id)
        sio.emit("current_game_state", match_dto.model_dump(by_alias=True), to=sid)

    @sio.event
    @with_app_context
    def rejoin_game(sid: str):  # pyright: ignore[reportUnusedFunction]
        user_id = get_user_id_by_sid_from_cache(sid)
        match_dto: MatchDto = game_service.get_active_game(user_id, "MP")

        sio.enter_room(sid, cast(UUID, match_dto.id))
        sio.emit("current_game_state", match_dto.model_dump(by_alias=True), to=sid)

    @sio.event
    @with_app_context
    def make_player_move(sid: str, data: dict[Any, Any]):  # pyright: ignore[reportUnusedFunction]
        user_id = get_user_id_by_sid_from_cache(sid)
        player_move = PlayerMoveDto(**data)
        match_dto: MatchDto = game_service.make_player_move(user_id, player_move, "MP")

        sio.emit("current_game_state", match_dto.model_dump(by_alias=True), room=cast(UUID, match_dto.id))

    @sio.event
    @with_app_context
    def leave_game(sid: str):  # pyright: ignore[reportUnusedFunction]
        user_id = get_user_id_by_sid_from_cache(sid)
        match_id = cast(UUID, get_match_by_user_id_from_cache(user_id, "MP").id)
        sio.leave_room(sid, match_id)
