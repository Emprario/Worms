"""
Point d'entrée dans le programme
Ce module devra également contenir
    - Les instructions pour lancer la boucle principale (dans game_engine.MaitreDuJeu)
"""

import pygame
from map import TileMap
from worms import Worm

# Initialize Pygame
pygame.init()

# Set up the screen and map
path = "assets/map/01.map"
map = TileMap(path)
SCREEN = pygame.display.set_mode(map.dimensions)
pygame.display.set_caption("PalaVect2")

# Set up color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

player = Worm(0,500,300)

# Main game loop
run = True
while run:
    # Handle events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(1)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_worm(-1, 0)
    if keys[pygame.K_RIGHT]:
        player.move_worm(1, 0)

    # Game logic (update)

    # Render (draw)
    SCREEN.fill(WHITE)
    map.print_map(map.map, SCREEN)
    player.draw(SCREEN)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
