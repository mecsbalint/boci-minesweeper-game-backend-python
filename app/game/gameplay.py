from random import choice
from app.error_handling.exceptions import InvalidBoardException, InvalidPlayerMoveException
from app.game.game import ActionType, Cell, Game, Coordinates, Player


def populate_with_mines(board: dict[Coordinates, Cell], num_of_mines: int, *, start_cell: Cell | None = None):
    valid_cells: list[Cell] = []
    if start_cell:
        valid_cells = [*set(board.values()) & {start_cell, *start_cell.neighbors}]
    else:
        valid_cells = [*board.values()]

    if len(valid_cells) < num_of_mines:
        raise InvalidBoardException()

    for _ in range(num_of_mines):
        cell = choice(valid_cells)
        cell.is_mine = True
        valid_cells.remove(cell)
        for neighbor in cell.neighbors:
            neighbor.num_neighbor_mines += 1


def handle_player_step(game: Game, action_type: ActionType, action_coordinates: Coordinates, player: Player):
    action_cell = game.board.get(action_coordinates)
    if not action_cell or action_cell.owner or player not in game.players:
        raise InvalidPlayerMoveException()

    match action_type:
        case ActionType.REVEAL:
            __handle_reveal_action(game, action_cell, player)
        case ActionType.FLAG:
            __handle_flag_action(action_cell, player)


def __handle_reveal_action(game: Game, action_cell: Cell, player: Player) -> None:
    action_cell.owner = player
    if action_cell.is_mine:
        game.players.remove(player)
    else:
        __reveal_cell_block(game, action_cell, player)


def __handle_flag_action(action_cell: Cell, player: Player) -> None:
    if player in action_cell.flagged_by:
        action_cell.flagged_by.remove(player)
    elif player not in action_cell.flagged_by:
        action_cell.flagged_by.add(player)


def __reveal_cell_block(game: Game, starting_cell: Cell, player: Player) -> None:
    cells_to_check = {starting_cell}

    while len(cells_to_check) > 0:
        cells_to_check_next: set[Cell] = set()
        for cell in cells_to_check:
            cell.owner = player
            if cell.num_neighbor_mines == 0:
                cells_to_check_next.update([
                    neighbor
                    for neighbor in cell.neighbors
                    if not neighbor.owner and player not in neighbor.flagged_by
                    ])
        cells_to_check = cells_to_check_next


def check_for_finish(game: Game) -> bool:
    if len(game.players) <= 1:
        return True

    has_not_owned_not_mines: bool = False

    for cell in game.board.values():
        if not cell.owner and not cell.is_mine:
            has_not_owned_not_mines = True

    return has_not_owned_not_mines


def check_for_winner(game: Game) -> Player | None:
    candidates = {player: 0 for player in game.players if player.active}

    if len(candidates) == 0:
        return None

    for cell in game.board.values():
        if cell.owner in candidates:
            candidates[cell.owner] += 1

    return max(candidates, key=lambda candidate: candidates[candidate])
