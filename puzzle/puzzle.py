class Puzzle:
    def __init__(self, size: int) -> None:
        self._size = size
        # A 2D matrix representing the tiles of the puzzle.
        # Each tile is either an int that identifies it or None (empty tile)
        self._puzzle: list[list[int | None]] = []
        # Create the completed puzzle (tiles are in order, last one is empty)
        for i in range(1, self.tiles_cnt + 1):
            if (i - 1) % 3 == 0:
                self._puzzle.append([])
            self._puzzle[-1].append(i if i < self.tiles_cnt else None)

    @property
    def size(self) -> int:
        return self._size

    @property
    def tiles_cnt(self) -> int:
        return self._size**2

    def _is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self._size and 0 <= y < self._size

    def get_tile_coords(self, tile: int | None) -> tuple[int, int] | None:
        for x in range(self._size):
            for y in range(self._size):
                if self._puzzle[y][x] == tile:
                    return (x, y)
        return None

    def get_tile_at_coords(self, x: int, y: int) -> int | None:
        if not self._is_within_bounds(x, y):
            return None
        return self._puzzle[y][x]

    def calc_available_moves(self) -> list[tuple[int, int]]:
        moves: list[tuple[int, int]] = []
        empty_coords = self.get_tile_coords(None)
        if empty_coords is None:
            return False
        x, y = empty_coords
        # Check for adiacent tiles in order: up, right, down, left
        for x_offset, y_offset in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            cur_x = x + x_offset
            cur_y = y + y_offset
            if self._is_within_bounds(cur_x, cur_y):
                moves.append((cur_x, cur_y))
        return moves

    def swap_tiles(self, x_a: int, y_a: int, x_b: int, y_b: int) -> bool:
        if not self._is_within_bounds(x_a, y_a) or not self._is_within_bounds(x_b, y_b):
            return False
        self._puzzle[y_a][x_a], self._puzzle[y_b][x_b] = self._puzzle[y_b][x_b], self._puzzle[y_a][x_a]
        return True

    def move_tile(self, x: int, y: int) -> bool:
        if (x, y) not in self.calc_available_moves():
            return False
        empty_coords = self.get_tile_coords(None)
        if empty_coords is None:
            return False
        self.swap_tiles(x, y, *empty_coords)
        return True

    def cmp(self, other: "Puzzle") -> bool:
        if self._size != other._size:
            return False
        for x in range(self._size):
            for y in range(self._size):
                if self._puzzle[y][x] != other._puzzle[y][x]:
                    return False
        return True

    def clone(self) -> "Puzzle":
        clone = Puzzle(self._size)
        clone._puzzle = [row.copy() for row in self._puzzle]
        return clone

    def calc_solution(self) -> list["Puzzle"]:
        # Import the function here to avoid circular imports
        from .solver import a_star
        return a_star(self, Puzzle(self._size))
