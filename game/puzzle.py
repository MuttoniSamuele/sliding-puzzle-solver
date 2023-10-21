class Puzzle:
    def __init__(self, size: int) -> None:
        self._size = size
        # A 2D matrix representing the tiles of the puzzle.
        # Each tile is either an int that identifies it or None (empty tile)
        self.puzzle: list[list[int | None]] = []
        tiles_cnt = size**2
        # Create the completed puzzle (tiles are in order, last one is empty)
        for i in range(1, tiles_cnt + 1):
            if (i - 1) % 3 == 0:
                self.puzzle.append([])
            self.puzzle[-1].append(i if i < tiles_cnt else None)

    def _is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self._size and 0 <= y < self._size

    def _get_adiacent_empty_tile(self, x: int, y: int) -> tuple[int, int] | None:
        if not self._is_within_bounds(x, y):
            return None
        # Check for empty tiles in order: up, right, down, left
        for x_offset, y_offset in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            cur_x = x + x_offset
            cur_y = y + y_offset
            if self._is_within_bounds(cur_x, cur_y) and self.puzzle[cur_y][cur_x] == None:
                return (cur_x, cur_y)
        return None

    def swap(self, x_a: int, y_a: int, x_b: int, y_b: int) -> bool:
        if not self._is_within_bounds(x_a, y_a) or not self._is_within_bounds(x_b, y_b):
            return False
        self.puzzle[y_a][x_a], self.puzzle[y_b][x_b] = self.puzzle[y_b][x_b], self.puzzle[y_a][x_a]
        return True

    def move_tile(self, x: int, y: int) -> bool:
        empty_coords = self._get_adiacent_empty_tile(x, y)
        if empty_coords is None:
            return False
        self.swap(x, y, *empty_coords)
        return True
