"""
Point d'entrée dans le programme
Ce module devra également contenir
    - Les instructions pour lancer la boucle principale (dans game_engine.MaitreDuJeu)
"""
from threading import Thread

import pygame

from map import TileMap
from debug_pygame import show_point, get_point_from_idx
from debug_utils import get_time_incache

pygame.init()

path = "assets/map/01.map"
map = TileMap(path)

SCREEN = pygame.display.set_mode(map.dimensions)

pygame.display.set_caption("PalaVect2")

Oclock = pygame.time.Clock()

run = True
debug_switch = False

map.blit_texture(SCREEN, all_pxs=True)

while run:
    destruction = ()
    if debug_switch:
        map.print_map(SCREEN)
    else:
        map.blit_texture(SCREEN)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                debug_switch = not debug_switch
                map.blit_texture(SCREEN, all_pxs=True)
            if event.key == pygame.K_d:
                get_time_incache()
            elif event.key == pygame.K_ESCAPE:
                run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse point @", pygame.mouse.get_pos())
            destruction = (pygame.mouse.get_pos(), 50.0)
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit(1)

    if destruction != ():
        Thread(group=None, target=map.destroy_map, name=None, args=destruction).start()

    Oclock.tick(60)
