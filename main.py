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
from CONSTS import FRAMERATE
from physics import all_moves, translation
from weapon import Projectile
from worms import Worm

pygame.init()

path = "assets/map/01.map"
map = TileMap(path)

flags = pygame.FULLSCREEN | pygame.HWSURFACE
SCREEN = pygame.display.set_mode(map.dimensions, flags)

pygame.display.set_caption("PalaVect2")

Oclock = pygame.time.Clock()
tick = 0

debug_switch = False
fps = 0

map.blit_texture(all_pxs=True)

all_sprites = pygame.sprite.Group()
# obstacles = pygame.sprite.Group()

player = Worm(0,680,358)

run = True
while run:
    destruction = ()
    if debug_switch:
        map.print_map()
    else:
        map.blit_texture()
    SCREEN.blit(map.Surf, (0, 0))
    tt = (map.Surf, (0, 0))
    SCREEN.blit(*tt)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                debug_switch = not debug_switch
                map.blit_texture(all_pxs=True)
            elif event.key == pygame.K_d:
                get_time_incache()
                print("Available :", map.available_ONMAPs)
                print("To clean :", map.clear_ONMAPs)
            elif event.key == pygame.K_f:
                map = TileMap(path)
                map.blit_texture(all_pxs=True)
            elif event.key == pygame.K_ESCAPE:
                run = False

            elif event.key == pygame.K_SPACE:
                projectile = Projectile(map.dimensions[0]// 2, map.dimensions[1]//2, "")
                all_sprites.add(projectile)
                projectile.add_to_move(all_moves, map.map)
                projectile.launched = True
                print("missile launched")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse point @", pygame.mouse.get_pos())
            circle = get_circle(5, pos := pygame.mouse.get_pos(), radius := 40)
            map.destruction_stack.append((pygame.mouse.get_pos(), 40.0))
            map.destruction_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit(1)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_worm(-1, 0)
    if keys[pygame.K_RIGHT]:
        player.move_worm(1, 0)
    player.draw(SCREEN)
    # Upadte dezs sprites
    for sprite in all_sprites:
        # if isinstance(projectile, Projectile) and projectile.launched:
        #     collisions = pygame.sprite.spritecollide(projectile, obstacles, True)
        #     if collisions:
        #         projectile.kill()
        # Affichage
        print(sprite.x, sprite.y)
        SCREEN.blit(sprite.image, (sprite.x, sprite.y))



    map.void_destruction_stack()

    for i in range(len(all_moves)):
        result = translation(*all_moves[i][:-1])
        all_moves[i][-3] = result[1]
        if not result[0]:
            all_moves[i][-1](*all_moves[i][:-1], result[2])
            del all_moves[i]

    pygame.display.flip()
    Oclock.tick(FRAMERATE)
    tick += 1

    # if fps != Oclock.get_fps() and (fps := Oclock.get_fps()) < 60 and fps != 0:
    #    print(f"/!\\ Low tick /!\\ framerate@{fps}")
