"""
Module de debug
"""
DEBUG_FLAG: bool = False

import pygame

SIZE = (1080, 920)

pygame.init()
DEBUG_SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Debug screen")


def show_point(point):
    global DEBUG_FLAG
    pygame.draw.circle(DEBUG_SCREEN, (255, 0, 0), point, 5)
    pygame.display.flip()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                DEBUG_FLAG = not DEBUG_FLAG
                print("Set DEBUG_FLAG to",DEBUG_FLAG)
            elif event.type == pygame.KEYDOWN:
                run = False


def clear_screen():
    pygame.draw.rect(DEBUG_SCREEN, (0, 0, 0), pygame.Rect(0, 0, *SIZE))
