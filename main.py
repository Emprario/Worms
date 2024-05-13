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
import pygame

from entity import Entity
from map import TileMap
from debug_utils import get_time_incache
from menu import Button, Menu
from CONSTS import FRAMERATE, MENU_SIZE
from physics import all_moves, translation
from worms import Worm


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PalaVect2")

        self.path = "assets/map/01.map"
        self.map = TileMap(self.path)

        # flags = pygame.FULLSCREEN | pygame.HWSURFACE
        self.SCREEN = pygame.display.set_mode(self.map.dimensions)  # , flags)
        self.ACTIVE_MENU: Menu = None

        self.Oclock = pygame.time.Clock()
        self.tick = 0
        self.fps = 0

        self.map.blit_texture(all_pxs=True)

        self.all_sprites: set[Entity] = set()

        self.current_player = 0
        self.players: list[Worm] = [Worm(0, 680, 358), Worm(0, 950, 358)]

        self.running = False
        self.pause = False

        self.PAUSE_MENU = None
        self.create_menus()

    def create_menus(self):
        resume_button = Button(304, 125, pygame.image.load("assets/menu/buttons/resume.png").convert_alpha(), 1,
                               self.exit_menu)
        options_button = Button(297, 250, pygame.image.load("assets/menu/buttons/options.png").convert_alpha(), 1,
                                None)
        quit_button = Button(336, 375, pygame.image.load("assets/menu/buttons/quit.png").convert_alpha(), 1,
                             self.exit_game)

        self.PAUSE_MENU = Menu("Pause", MENU_SIZE[0], MENU_SIZE[1], None, [resume_button, options_button, quit_button])

    def exit_game(self):
        self.running = False

    def exit_menu(self):
        self.ACTIVE_MENU = None

    def next_player(self):
        self.current_player += 1
        self.current_player %= len(self.players)

    def run(self):
        self.running = True
        for player in self.players:
            self.all_sprites.add(player)

        # ----------------- Boucle principale --------------------
        while self.running:
            if self.ACTIVE_MENU is not None:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.ACTIVE_MENU.onClick(pygame.mouse.get_pos())
            else:
                self.map.blit_texture()
                self.SCREEN.blit(self.map.Surf, (0, 0))

                # ------------- Gestion des événements -------------------
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_o:
                            get_time_incache()
                            print("Available :", self.map.available_ONMAPs)
                            print("To clean :", self.map.clear_ONMAPs)
                        elif event.key == pygame.K_m:
                            self.next_player()
                        elif event.key == pygame.K_ESCAPE:
                            self.exit_game()
                        elif event.key == pygame.K_p:
                            self.ACTIVE_MENU = self.PAUSE_MENU
                            self.ACTIVE_MENU.draw(self.SCREEN)
                        # elif event.key == pygame.K_f:
                        #    self.map = TileMap(self.path)
                        #    self.map.blit_texture(all_pxs=True)

                # ------------- Affichage des Entités --------------------
                for sprite in self.all_sprites:
                    self.SCREEN.blit(sprite.image, (sprite.x - sprite.offset_x, sprite.y - sprite.offset_y))

                # ------------- Execution des explosions -----------------
                self.map.void_destruction_stack()

                # ------------- Mouvement des joueurs --------------------
                x_movement = 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    x_movement = -2
                if keys[pygame.K_d]:
                    x_movement = 2
                self.players[self.current_player].move_worm(x_movement, 0, self.map.map, all_moves, self.tick)
                for i in range(len(self.players)):
                    if i != self.current_player:
                        self.players[i].move_worm(0, 0, self.map.map, all_moves, self.tick)

                # ------------- Déplacement des Entités ------------------
                i = 0
                while i < len(all_moves):
                    print(self.tick, [move[3] for move in all_moves])
                    result = translation(*all_moves[i][:-2], self.tick - all_moves[i][-2])
                    # print(result)
                    all_moves[i][-3] = result[1]
                    if result[0]:
                        print("I: Killed")
                        all_moves[i][-1](*all_moves[i][:-1], result[2])
                        del all_moves[i]
                    else:
                        i += 1

                # -------------- Actualisation pygame --------------------
                pygame.display.flip()
                self.Oclock.tick(FRAMERATE)
                self.tick += 1

                # if fps != Oclock.get_fps() and (fps := Oclock.get_fps()) < 60 and fps != 0:
                #    print(f"/!\\ Low tick /!\\ framerate@{fps}")
        pygame.quit()


if __name__ == "__main__":
    theGame = Game()
    theGame.run()
