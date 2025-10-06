from typing import Any, cast
from app.cache.lobby_cache import get_lobby
from app.cache.match_cache import get_matches_by_ids_from_cache
from app.dto.game_dto import MatchLobbyDto
from app.service.user_service import get_user_by_id


def create_match_lobby_dto_dicts() -> list[dict[str, Any]]:
    match_ids = get_lobby()
    match_set = get_matches_by_ids_from_cache(match_ids, "MP")

    lobby_dto_dicts: list[dict[str, Any]] = list()

    for match in match_set:
        owner_user = get_user_by_id(cast(int, match.match_owner))
        owner_name = cast(str, owner_user.name) if owner_user else None
        lobby_dto_dicts.append(MatchLobbyDto.from_match(match, owner_name).model_dump(by_alias=True))

    return lobby_dto_dicts
