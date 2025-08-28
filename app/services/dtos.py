from app.game.models import Game, Cell, GameState
from typing import Literal


class JwtResponseDto:
    def __init__(self, jwt: str, user_name: str):
        self.jwt = jwt
        self.user_name = user_name


class PlayerMoveDto:
    def __init__(self, coordinates: dict[Literal["x", "y"], int], action_type: Literal["REVEAL", "FLAG"]):
        self.coordinates = coordinates
        self.action_type = action_type


class GameDto:
    def __init__(self, game: Game):
        self.state = game.state.name
        self.rows = game.rows
        self.columns = game.columns
        self.cells = {coordinates: CellDto(cell, game.state) for coordinates, cell in game.cells.items()}


class CellDto:
    def __init__(self, cell: Cell, game_state: GameState):
        self.state = CellDto.__get_state(cell, game_state)

    @staticmethod
    def __get_state(cell: Cell, game_state: GameState) -> str:
        match game_state:
            case GameState.INITIALIZED:
                return "hidden"
            case GameState.STARTED:
                return CellDto.__get_state_for_started(cell)
            case GameState.FINISHED_WON:
                return CellDto.__get_state_for_finished_won(cell)
            case GameState.FINISHED_LOST:
                return CellDto.__get_state_for_finished_lost(cell)

    @staticmethod
    def __get_state_for_started(cell: Cell) -> str:
        if cell.is_flagged:
            return "flagged"
        elif cell.is_hidden:
            return "hidden"
        elif cell.is_mine:
            return "mine"
        elif cell.num_neighbor_mines > 0:
            return str(cell.num_neighbor_mines)
        else:
            return "empty"

    @staticmethod
    def __get_state_for_finished_won(cell: Cell) -> str:
        if cell.is_mine:
            return "mine"
        elif cell.num_neighbor_mines > 0:
            return str(cell.num_neighbor_mines)
        else:
            return "empty"

    @staticmethod
    def __get_state_for_finished_lost(cell: Cell) -> str:
        if cell.is_mine:
            return "mine"
        elif cell.is_hidden:
            return "hidden"
        elif cell.num_neighbor_mines > 0:
            return str(cell.num_neighbor_mines)
        else:
            return "empty"
