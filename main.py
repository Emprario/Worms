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
from utils import get_circle

pygame.init()

path = "assets/map/01.map"
map = TileMap(path)

flags = pygame.FULLSCREEN | pygame.HWSURFACE
SCREEN = pygame.display.set_mode(map.dimensions, flags)

pygame.display.set_caption("PalaVect2")

Oclock = pygame.time.Clock()

run = True
debug_switch = False
fps = 0

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
            elif event.key == pygame.K_d:
                get_time_incache()
                print("Available :", map.available_ONMAPs)
                print("To clean :", map.clear_ONMAPs)
            elif event.key == pygame.K_f:
                map = TileMap(path)
                map.blit_texture(SCREEN, all_pxs=True)
            elif event.key == pygame.K_ESCAPE:
                run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse point @", pygame.mouse.get_pos())
            circle = get_circle(10, pos := pygame.mouse.get_pos(), radius := 40)
            map.destruction_stack.append((pygame.mouse.get_pos(), radius))
            map.destruction_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit(1)

    map.void_destruction_stack()

    # Oclock.tick(144)

    #if fps != Oclock.get_fps() and (fps := Oclock.get_fps()) < 60 and fps != 0:
    #    print(f"/!\\ Low tick /!\\ framerate@{fps}")
