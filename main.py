"""
Point d'entrée dans le programme
Ce module devra également contenir
    - Les instructions pour lancer la boucle principale (dans game_engine.MaitreDuJeu)
"""

import pygame

from map import TileMap
from debug_pygame import show_point, get_point_from_idx

pygame.init()

path = "assets/map/01.map"
map = TileMap(path)

SCREEN = pygame.display.set_mode(map.dimensions)

pygame.display.set_caption("PalaVect2")

Oclock = pygame.time.Clock()

run = True
debug_switch = False
while run:
    if debug_switch:
        map.print_map(SCREEN)
    else:
        map.blit_texture(SCREEN)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                debug_switch = not debug_switch
            # if event.key == pygame.K_d:
            elif event.key == pygame.K_ESCAPE:
                run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse point @", pygame.mouse.get_pos())
            map.destroy_map(pygame.mouse.get_pos(), 50.0)
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit(1)
    # Oclock.tick(60)
