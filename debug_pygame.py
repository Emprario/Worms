"""
Outils de debug pour pygame
"""
import pygame

SIZE = (1920, 1080)

pygame.init()
DEBUG_SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Debug screen")


def get_point_from_idx(idx: int) -> tuple[int, int]:
    return (idx // 4) % SIZE[0], (idx // 4) // SIZE[0]


def show_point(point, *, color=(255, 0, 0), does_stop: bool = True, verbose: bool = False, one_pixel: bool = False):
    if verbose:
        print("highlihting", point)
    if not one_pixel:
        pygame.draw.circle(DEBUG_SCREEN, color, point, 5)
    else:
        DEBUG_SCREEN.set_at(point, color)
    pygame.display.flip()
    run = does_stop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
