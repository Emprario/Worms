"""
Point d'entrée dans le programme
Ce module devra également contenir
    - Les instructions pour lancer la boucle principale (dans game_engine.MaitreDuJeu)
"""

import pygame
from map import TileMap


pygame.init()

path = "assets/map/03.map"
map = TileMap(path)

SCREEN = pygame.display.set_mode(map.dimensions)

pygame.display.set_caption("PalaVect2")

run = True
while run:
    map.print_map(map.map, SCREEN)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse point @", pygame.mouse.get_pos())
            oldmap = map.map
            map.destroy_map(pygame.mouse.get_pos(), 200.0)
            print(oldmap == map.map)
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit(1)