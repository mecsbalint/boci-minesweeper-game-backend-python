from app.game.models import Game, Cell


class GameDto:
    def __init__(self, game: Game):
        self.state = game.state.name
        self.rows = game.rows
        self.columns = game.columns
        self.cells = [CellDto(cell) for cell in game.cells.values()]


class CellDto:
    def __init__(self, cell: Cell):
        self.coordinates = cell.coordinates
        self.state = self.__get_state(cell)

    def __get_state(cell: Cell) -> str:
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
