"""
Point d'entrée dans le programme
Ce module est divisé en trois partie
    * Importation des modules externes puis internes
    * Initialisation
    * Boucle Principale

La boucle principale est elle-même composé des  éléments suivants
    * Affichage de la map
    * Capture et réactions des events
    * Affichage des sprites
    * Vidage du stack des explosions
    * Execution des mouvements
    * Gestions des worms
    * Flip de l'écran
    * Calcul du framerate
"""
from threading import Thread

import pygame

from map import TileMap
from debug_pygame import show_point, get_point_from_idx
from debug_utils import get_time_incache
from utils import get_circle
from CONSTS import FRAMERATE
from physics import move_entities, addtomove, def_map
from weapon import Pro_bazooka
from weapon import Bazooka
from weapon import Pro_sniper
from weapon import Pro_grenade
from weapon import Pro_frag_grenade
from worms import Worm
from math import pi
from weapon import  Charg_bar

pygame.init()

path = "assets/map/01.map"
map = TileMap(path)
def_map(map)

flags = pygame.FULLSCREEN | pygame.HWSURFACE
SCREEN = pygame.display.set_mode(map.dimensions, flags)

pygame.display.set_caption("PalaVect2")

Oclock = pygame.time.Clock()
tick = 0

debug_switch = False
fps = 0

map.blit_texture(all_pxs=True)

all_sprites = pygame.sprite.Group()

actual_weapon = 0
inclinaison = 0.0
power = 0.1

player = Worm(0,680,358)

bazooka = Bazooka((map.dimensions[0] // 2)-30, (map.dimensions[1] // 2)-30, "assets/textures/Bazooka.png", -30)
all_sprites.add(bazooka)
charg_bar = Charg_bar((map.dimensions[0] // 2)-30, (map.dimensions[1] // 2)-60)
all_sprites.add(charg_bar)

run = True
while run:
    destruction = ()

    if debug_switch:
        map.print_map()
    else:
        map.blit_texture()
    SCREEN.blit(map.Surf, (0, 0))


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
            elif event.key == pygame.K_e:
                if actual_weapon <= 2:
                    actual_weapon += 1
                else:
                    actual_weapon = 0
            elif event.key == pygame.K_UP:
                inclinaison -= 0.1
                bazooka.rotate(0.1*360/(2*pi))
            elif event.key == pygame.K_DOWN:
                inclinaison += 0.1
                bazooka.rotate(-0.1 * 360 / (2 * pi))
            elif event.key == pygame.K_SPACE:
                if actual_weapon == 1:
                    pro_sniper = Pro_sniper(map.dimensions[0] // 2, map.dimensions[1] // 2, "", map.destruction_stack,25, 5, False)
                    all_sprites.add(pro_sniper)
                    addtomove(power * pro_sniper.speed, inclinaison, pro_sniper, pro_sniper.destroy)
                    pro_sniper.launched = True
                    print("missile launched")

                if actual_weapon == 0 or actual_weapon == 2 or actual_weapon == 3:
                    power = -tick * 0.015
                    charg_bar.agrandissement = True
                    charge = power
                    charg_bar.up_taille(10)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                power += tick * 0.015 + 0.2
                if power > 1:
                    power = 1
                if actual_weapon == 0:
                    pro_bazooka = Pro_bazooka(map.dimensions[0] // 2, map.dimensions[1] // 2, "", map.destruction_stack,12,20,False)
                    all_sprites.add(pro_bazooka)
                    addtomove(power * pro_bazooka.speed, inclinaison, pro_bazooka, pro_bazooka.destroy)
                    pro_bazooka.launched = True
                elif actual_weapon == 2:
                    pro_grenade = Pro_grenade(map.dimensions[0] // 2, map.dimensions[1] // 2, "", map.destruction_stack,7, 10, True)
                    all_sprites.add(pro_grenade)
                    addtomove(power * pro_grenade.speed, inclinaison, pro_grenade, pro_grenade.destroy)
                    pro_grenade.launched = True
                elif actual_weapon == 3:
                    pro_frag_grenade = Pro_frag_grenade(map.dimensions[0] // 2, map.dimensions[1] // 2, "",map.destruction_stack, 7,10,True)
                    all_sprites.add(pro_frag_grenade)
                    addtomove(power * pro_frag_grenade.speed, inclinaison, pro_frag_grenade, pro_frag_grenade.destroy)
                    pro_frag_grenade.launched = True
                power = 0.2
                print("missile launched")
                charg_bar.agrandissement=False
                charg_bar.reset_taille()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse point @", pygame.mouse.get_pos())
            circle = get_circle(5, pos := pygame.mouse.get_pos(), radius := 40)
            map.destruction_stack.append((pygame.mouse.get_pos(), 40.0))
            map.destruction_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit(1)

    # Upadte des sprites
    for sprite in all_sprites:
        SCREEN.blit(sprite.image, (sprite.x, sprite.y))

    if charg_bar.agrandissement == True:
        charge = power + tick * 0.015 + 0.2
        if charge < 1:
            charg_bar.up_taille(3)

    # Execution des explosions
    map.void_destruction_stack()

    move_entities()

    #------------- Worms part ---------------------
    x_movement = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x_movement = -2
    if keys[pygame.K_RIGHT]:
        x_movement = 2
    player.move_worm(x_movement, 0, map.map)
    if keys[pygame.K_z]:
        player.jump_worm(tick, map.map)
    player.draw(SCREEN)
    #----------------------------------------------
    
    pygame.display.flip()
    Oclock.tick(FRAMERATE)
    tick += 1

    # if fps != Oclock.get_fps() and (fps := Oclock.get_fps()) < 60 and fps != 0:
    #    print(f"/!\\ Low tick /!\\ framerate@{fps}")
