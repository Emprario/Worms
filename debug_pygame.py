import pygame

SIZE = (1920, 1080)

pygame.init()
DEBUG_SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Debug screen")


def show_point(point, *, color=(255, 0, 0), does_stop: bool = True, verbose: bool = False):
    if verbose:
        print("highlihting", point)
    pygame.draw.circle(DEBUG_SCREEN, color, point, 5)
    pygame.display.flip()
    run = does_stop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
