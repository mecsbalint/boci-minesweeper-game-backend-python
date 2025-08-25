
class Game:
    def __init__(self, rows: int, columns: int, cells: list["Cell"]):
        self._rows = rows
        self._columns = columns
        self._cells = cells
        self._is_started = False


class Cell:
    def __init__(self, game: Game, coordinates: tuple[int, int], is_mine: bool, neighbors: list["Cell"]):
        self._game = game
        self._coordinates = coordinates
        self._is_mine = is_mine
        self._neighbors = neighbors
        self._is_hidden = True
        self._is_flagged = False
        self._num_neighbor_mines = self.count_neighbor_mines()

    def count_neighbor_mines(self):
        return len(filter(lambda cell: cell._is_mine, self._neighbors))
