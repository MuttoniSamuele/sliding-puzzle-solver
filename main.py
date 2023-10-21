import pygame


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Sliding Puzzle Solver")
    screen = pygame.display.set_mode((800, 600))
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
        if running:
            pygame.display.update()


if __name__ == "__main__":
    main()
