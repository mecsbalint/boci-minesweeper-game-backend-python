from random import choice
from typing import cast
from app.error_handling.exceptions import InvalidBoardException, InvalidPlayerMoveException
from app.game.game import ActionType, Cell, Game, Coordinates, Player


def populate_with_mines(board: dict[Coordinates, Cell], num_of_mines: int, *, action_coordinates: list[Coordinates] | None = None):
    valid_cells_set: set[Cell] = {*board.values()}
    if action_coordinates:
        invalid_cells: set[Cell] = set()
        for coordinates in action_coordinates:
            start_cell = cast(Cell, board.get(coordinates))
            if start_cell:
                invalid_cells.update({start_cell, *start_cell.neighbors})
            else:
                raise InvalidPlayerMoveException()
        valid_cells_set = valid_cells_set - invalid_cells

    if len(valid_cells_set) < num_of_mines:
        raise InvalidBoardException()

    valid_cells_list = [*valid_cells_set]
    for _ in range(num_of_mines):
        cell = choice(valid_cells_list)
        cell.is_mine = True
        valid_cells_list.remove(cell)
        for neighbor in cell.neighbors:
            neighbor.num_neighbor_mines += 1


def remove_mines(board: dict[Coordinates, Cell]):
    for cell in board.values():
        cell.is_mine = False
        cell.num_neighbor_mines = 0


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


def get_cell_block(game: Game, position: Coordinates) -> set[Cell]:
    block: set[Cell] = set()
    cells_to_check = {cast(Cell, game.board.get(position))}

    while len(cells_to_check) > 0:
        cells_to_check_next: set[Cell] = set()
        for cell in cells_to_check:
            block.add(cell)
            if cell.num_neighbor_mines == 0:
                cells_to_check_next.update([
                    neighbor
                    for neighbor in cell.neighbors
                    if neighbor not in block
                    ])
        cells_to_check = cells_to_check_next

    return block


def check_for_finish(game: Game) -> bool:
    if len(game.players) <= 1:
        return True

    for cell in game.board.values():
        if not cell.owner and not cell.is_mine:
            return False

    return True


def check_for_winner(game: Game) -> Player:
    if len(game.players) == 1:
        return list(game.players)[0]

    candidates = get_current_scores(game)

    return max(candidates, key=lambda candidate: candidates[candidate])


def get_current_scores(game: Game) -> dict[Player, int]:
    scores = {player: 0 for player in game.players if player is not Player.PLAYER_VOID}

    for cell in game.board.values():
        if cell.owner in scores:
            scores[cell.owner] += 1

    return scores
