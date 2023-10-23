from .puzzle import Puzzle


class Node:
    """A node of a stack used internally in the A* algorithm."""
    def __init__(self, parent: "Node | None", puzzle: Puzzle) -> None:
        self.puzzle = puzzle
        self.parent = parent
        # Distance between this node and the start node
        self.g: int = 0
        # Estimated distance from this node to the goal node (heuristic)
        self.h: int = 0

    @property
    def f(self) -> int:
        """Total cost of this node.\n
        `f = g + h`"""
        return self.g + self.h

    def calc_successors(self) -> list["Node"]:
        """Creates clones of this node based on the available moves without
        mutating the original puzzle."""
        successors: list[Node] = []
        for x, y in self.puzzle.calc_available_moves():
            clone = self.puzzle.clone()
            clone.move_tile(x, y)
            successors.append(Node(self, clone))
        return successors


def calc_heuristic(node: Node, goal_node: Node) -> float:
    """The heuristic function.\n
    Estimates the distance between a node and the goal."""
    heuristic = 0
    for tile in range(1, goal_node.puzzle.tiles_cnt + 1):
        # If its the last tile, then its empty
        if tile == goal_node.puzzle.tiles_cnt:
            tile = None
        coords = node.puzzle.get_tile_coords(tile)
        goal_coords = goal_node.puzzle.get_tile_coords(tile)
        if coords is None or goal_node is None:
            continue
        x_n, y_n = coords
        x_g, y_g = goal_coords
        # Calculate the Manhattan distance
        heuristic += abs(x_n - x_g) + abs(y_n - y_g)
    return heuristic


def a_star(start: Puzzle, goal: Puzzle) -> list[Puzzle] | None:
    """Performs the A* pathfinding algorithm.\n"""
    start_node = Node(None, start)
    goal_node = Node(None, goal)
    # A list of nodes that are candidates for further exploration
    open_list: list[Node] = [start_node]
    # A list of nodes that have already been explored
    closed_list: list[Node] = []
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        # Find the node with the lowest f (best node)
        for i, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = i
        # Set the current node as explored
        open_list.pop(current_index)
        closed_list.append(current_node)
        # Check if the goal was reached
        if current_node.puzzle.cmp(goal_node.puzzle):
            # Traverse the nodes backwards until the start node is reached
            # while storing each puzzle state in a list
            path: list[Puzzle] = []
            while current_node is not None:
                path.append(current_node.puzzle)
                current_node = current_node.parent
            # Return the reversed path
            return path[::-1]
        # Loop through the current node's successors
        for successor_node in current_node.calc_successors():
            # Skip if the successor has already been explored
            in_closed = False
            for node in closed_list:
                if successor_node.puzzle.cmp(node.puzzle):
                    in_closed = True
                    break
            if in_closed:
                continue
            # Calculate this successor's g and h
            successor_node.g = current_node.g + 1
            successor_node.h = calc_heuristic(successor_node, goal_node)
            # If the successor isn't in the open list already, add it
            in_open = False
            for node in open_list:
                if successor_node.puzzle.cmp(node.puzzle):
                    in_open = True
                    # If the successor is already in the open list, check if its current g
                    # is better than the previous one and, in that case, update its g with the
                    # new value and set its parent to the current node
                    if successor_node.g < node.g:
                        node.g = successor_node.g
                        node.parent = current_node
            if in_open:
                continue
            open_list.append(successor_node)
    # No solutions found
    return None
