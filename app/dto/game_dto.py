from app.dto.dto_base_model import DtoBaseModel
from app.game.game import Cell, Coordinates, GameType, MapType, Player
from app.game.match import Match, MatchState
from typing import Literal


class MatchIdDto(DtoBaseModel):
    id: str


class GameStatusDto(DtoBaseModel):
    status: bool


class PlayerMoveDto(DtoBaseModel):
    coordinates: dict[Literal["x", "y"], int]
    action_type: Literal["REVEAL", "FLAG"]


class MatchLobbyDto(DtoBaseModel):
    id: str | None
    empty_seats: int
    max_num_of_players: int
    owner_name: str | None
    map_type: MapType
    game_type: GameType

    @classmethod
    def from_match(cls, match: Match, owner_name: str | None):
        max_num_of_players = len([p for p in match.game.players if p is not Player.PLAYER_VOID])
        empty_seats = max_num_of_players - len(match.participants)
        return cls(
            id=str(match.id),
            empty_seats=empty_seats,
            max_num_of_players=max_num_of_players,
            owner_name=owner_name,
            map_type=match.game.map_type,
            game_type=match.game.game_type
            )


class MatchDto(DtoBaseModel):
    id: str | None
    state: str
    winner_id: int | None
    board: list[list[str]]
    scoreboard: dict[str, int]

    @classmethod
    def from_match(cls, match: Match, user_id: int):
        state = match.state.name
        winner_id = None if not match.winner else match.winner.user_id
        current_player = next((p.player for p in match.participants if user_id == p.user_id))
        board = cls._generate_2d_list_from_board(match.game.board, match.state, current_player)
        scoreboard = {participant.user_name: participant.score for participant in match.participants}
        return cls(id=str(match.id), state=state, winner_id=winner_id, board=board, scoreboard=scoreboard)

    @staticmethod
    def _generate_2d_list_from_board(board: dict[Coordinates, Cell], match_state: MatchState, current_player: Player) -> list[list[str]]:
        rows = max(coor.y for coor in board) + 1
        columns = max(coor.x for coor in board) + 1

        list_2d = [["void" for _ in range(columns)] for _ in range(rows)]

        for coor, cell in board.items():
            list_2d[coor.y][coor.x] = MatchDto._get_state(cell, match_state, current_player)

        return list_2d

    @staticmethod
    def _get_state(cell: Cell, match_state: MatchState, current_player: Player) -> str:
        match match_state:  # pyright: ignore[reportMatchNotExhaustive]
            case MatchState.READY:
                return MatchDto._get_state_for_ready(cell, current_player)
            case MatchState.ACTIVE:
                return MatchDto._get_state_for_active(cell, current_player)
            case MatchState.FINISHED:
                return MatchDto._get_state_for_finished(cell, current_player)
            case _:
                return "void"

    @staticmethod
    def _get_state_for_ready(cell: Cell, current_player: Player) -> str:
        if current_player in cell.flagged_by:
            return "flagged"
        else:
            return "hidden"

    @staticmethod
    def _get_state_for_active(cell: Cell, current_player: Player) -> str:
        if current_player in cell.flagged_by:
            return "flagged"
        elif not cell.owner:
            return "hidden"
        elif current_player is not cell.owner:
            return f"opponent_{cell.owner.name}"
        elif cell.num_neighbor_mines == 0:
            return "empty"
        else:
            return str(cell.num_neighbor_mines)

    @staticmethod
    def _get_state_for_finished(cell: Cell, current_player: Player) -> str:
        if cell.is_mine:
            return "mine" if not cell.owner else "mine_activated"
        elif not cell.owner:
            return "neutral_" + ("empty" if cell.num_neighbor_mines == 0 else str(cell.num_neighbor_mines))
        elif current_player is not cell.owner:
            return f"opponent_{cell.owner.name}"
        elif cell.num_neighbor_mines == 0:
            return "empty"
        else:
            return str(cell.num_neighbor_mines)


MatchDtoDict = dict[int, MatchDto]
