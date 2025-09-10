from app.error_handling.exceptions import InvalidPlayerMoveException
from app.game.generation import populate_with_mines
from app.game.models import ActionType, Cell, Game, Coordinates, GameState
from typing import Iterable


def handle_player_step(game: Game, action_type: ActionType, action_coordinates: Coordinates):
    action_cell = game.cells.get(action_coordinates)
    if not action_cell or not action_cell.is_hidden:
        raise InvalidPlayerMoveException()

    match action_type:
        case ActionType.REVEAL:
            handle_reveal_action(game, action_coordinates)
        case ActionType.FLAG:
            handle_flag_action(game, action_coordinates)


def handle_reveal_action(game: Game, action_coordinates: Coordinates) -> None:
    if game.state.name == "INITIALIZED":
        populate_with_mines(game.cells, action_coordinates)
        game.state = GameState.STARTED

    action_cell = game.cells[action_coordinates]
    action_cell.is_hidden = False
    if action_cell.is_mine:
        game.state = GameState.FINISHED_LOST
    else:
        __reveal_cell_block(game, action_cell)
        if __check_for_winning(game.cells.values()):
            game.state = GameState.FINISHED_WON


def handle_flag_action(game: Game, action_coordinates: Coordinates) -> None:
    action_cell = game.cells[action_coordinates]
    if action_cell.is_flagged:
        action_cell.is_flagged = False
    elif action_cell.is_hidden:
        action_cell.is_flagged = True


def __reveal_cell_block(game: Game, starting_cell: Cell) -> None:
    cells_to_check = {starting_cell}

    while len(cells_to_check) > 0:
        cells_to_check_next: set[Cell] = set()
        for cell in cells_to_check:
            cell.is_hidden = False
            if cell.num_neighbor_mines == 0:
                cells_to_check_next.update([
                    neighbor
                    for neighbor in cell.neighbors
                    if neighbor.is_hidden and not neighbor.is_flagged
                    ])
        cells_to_check = cells_to_check_next


def __check_for_winning(cells: Iterable[Cell]) -> bool:
    for cell in cells:
        if cell.is_hidden and not cell.is_mine:
            return False
    return True
