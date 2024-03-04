"""
Point d'entrée dans le programme
Ce module devra également contenir
    - Les instructions pour lancer la boucle principale (dans game_engine.MaitreDuJeu)
"""
import pygame
import sys
from CONSTS import VERSION
from map import Map
from entity import  Entity
from worms import Worm

if __name__ == "__main__":
    print(f"Wormy version: {VERSION}")

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# Set up color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

mapobj = Map("assets/map/dummy.map")
Entity(mapobj)

player = Worm(0,50,50)


# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_worm(-1,0)
    if keys[pygame.K_RIGHT]:
        player.move_worm(1,0)


    # Game logic (update)

    # Render (draw)
    screen.fill(WHITE)
    mapobj.print_map(screen)
    player.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()