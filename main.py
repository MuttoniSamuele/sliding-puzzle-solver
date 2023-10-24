import pygame

from puzzle import Puzzle
from components import Button


def main() -> None:
    pygame.init()
    # Create the window
    pygame.display.set_caption("Sliding Puzzle Solver")
    screen = pygame.display.set_mode((800, 600))
    # Create the components
    btn = Button(screen, 20, 20, text="Click me")
    # Main loop
    running = True
    while running:
        # Handle events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
        btn.update_events(events)
        # Exit if the user quits (necessary because sometimes pygame unsyncs)
        if not running:
            break
        # Draw the components
        btn.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
