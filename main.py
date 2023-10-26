import pygame

from threading import Thread

from puzzle import Puzzle
from components import Button, colors


PUZZLE_SIZE = 540
PUZZLE_MARGIN = 30
BIG_BTN_WIDTH = 170
BTN_HEIGHT = 28
BIG_BTN_SPAN = 15
SMALL_BTN_WIDTH = 70
SMALL_BTN_MARGIN = 30
SMALL_BTN_SPAN = 50
TILE_SIZE = 156
TILE_MARGIN = 18
TILES_CONTAINER_COL = colors.NEUTRAL_700
TILE_BG_COL = colors.NEUTRAL_400,
TILE_HOVER_COL =colors.NEUTRAL_300,
TILE_ACTIVE_COL =colors.NEUTRAL_200


BTN_STYLE = {
    "font": pygame.font.SysFont("Calibri", 20),
    "border_radius": 3,
    "fg_color": colors.NEUTRAL_800,
    "bg_color": colors.NEUTRAL_300,
    "hover_bg_color": colors.NEUTRAL_400,
    "active_bg_color": colors.NEUTRAL_500
}

BIG_BTN_STYLE = {
    "width": BIG_BTN_WIDTH,
    "height": BTN_HEIGHT,
    **BTN_STYLE
}

SMALL_BTN_STYLE = {
    "width": SMALL_BTN_WIDTH,
    "height": BTN_HEIGHT,
    **BTN_STYLE
}


class SolverThread(Thread):
    def __init__(self, puzzle: Puzzle) -> None:
        Thread.__init__(self)
        self._puzzle = puzzle
        self._solution: list[Puzzle] | None = None
        self._running = False

    @property
    def solution(self) -> list[Puzzle] | None:
        return self._solution

    def start_once(self) -> None:
        if self._running:
            return
        self.start()

    def run(self) -> None:
        self._running = True
        self._solution = self._puzzle.calc_solution()


def draw_tiles_container(screen: pygame.Surface) -> None:
    pygame.draw.rect(screen, TILES_CONTAINER_COL,
        (PUZZLE_MARGIN, PUZZLE_MARGIN, PUZZLE_SIZE, PUZZLE_SIZE),
        border_radius=10
    )


def update_puzzle_tiles(tiles_btns: list[Button], puzzle: Puzzle) -> None:
    for y in range(3):
        for x in range(3):
            btn = tiles_btns[y * 3 + x]
            match puzzle.get_tile_at_coords(x, y):
                case None:
                    btn.bg_color = btn.hover_bg_color = btn.active_bg_color = TILES_CONTAINER_COL
                    btn.text = ""
                case tile:
                    btn.bg_color = TILE_BG_COL,
                    btn.hover_bg_color = TILE_HOVER_COL,
                    btn.active_bg_color = TILE_ACTIVE_COL
                    btn.text = str(tile)


def main() -> None:
    pygame.init()

    # Initialize the puzzle
    puzzle = Puzzle(3)
    solution_step = 0
    solver_thread = SolverThread(puzzle)

    # Create the window
    pygame.display.set_caption("Sliding Puzzle Solver")
    screen = pygame.display.set_mode((800, 600))

    # Define the callabacks for the buttons

    def handle_edit() -> None:
        pass

    def handle_solve() -> None:
        solver_thread.start_once()

    def handle_back() -> None:
        nonlocal solution_step
        solution_step = max(0, solution_step - 1)

    def handle_forward() -> None:
        if solver_thread.solution is None:
            return
        nonlocal solution_step
        solution_step = min(solution_step + 1, len(solver_thread.solution) - 1)

    # Create the components
    btn_base_x = PUZZLE_SIZE + PUZZLE_MARGIN*2
    edit_btn = Button(
        screen,
        text="Edit",
        x=btn_base_x,
        y=PUZZLE_MARGIN + BIG_BTN_SPAN,
        callback=handle_edit,
        **BIG_BTN_STYLE
    )
    solve_btn = Button(
        screen,
        text="Solve",
        x=btn_base_x,
        y=edit_btn.y + BTN_HEIGHT + BIG_BTN_SPAN,
        callback=handle_solve,
        **BIG_BTN_STYLE
    )
    back_btn = Button(
        screen,
        text="<",
        x=btn_base_x,
        y=solve_btn.y + BTN_HEIGHT + SMALL_BTN_SPAN,
        callback=handle_back,
        **SMALL_BTN_STYLE
    )
    forward_btn = Button(
        screen,
        text=">",
        x=back_btn.x + SMALL_BTN_WIDTH + SMALL_BTN_MARGIN,
        y=back_btn.y,
        callback=handle_forward,
        **SMALL_BTN_STYLE
    )
    tiles_btns: list[Button] = []
    for y in range(3):
        for x in range(3):
            def handle_click() -> None:
                pass

            tiles_btns.append(Button(
                screen,
                font=pygame.font.SysFont("Arial", 64),
                x=PUZZLE_MARGIN + TILE_MARGIN*(x + 1) + TILE_SIZE*x,
                y=PUZZLE_MARGIN + TILE_MARGIN*(y + 1) + TILE_SIZE*y,
                width=TILE_SIZE,
                height=TILE_SIZE,
                border_radius=8,
                fg_color=colors.NEUTRAL_900,
                callback=handle_click
            ))

    # Main loop
    running = True
    while running:
        # Handle events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
        edit_btn.update_events(events)
        solve_btn.update_events(events)
        back_btn.update_events(events)
        forward_btn.update_events(events)
        [btn.update_events(events) for btn in tiles_btns]
        # Exit if the user quits (necessary because sometimes pygame unsyncs)
        if not running:
            break
        # Update the components
        update_puzzle_tiles(
            tiles_btns,
            puzzle if solver_thread.solution is None else solver_thread.solution[solution_step]
        )
        # Draw the components
        screen.fill(colors.NEUTRAL_800)
        draw_tiles_container(screen)
        edit_btn.draw()
        solve_btn.draw()
        back_btn.draw()
        forward_btn.draw()
        [btn.draw() for btn in tiles_btns]
        pygame.display.update()


if __name__ == "__main__":
    main()
