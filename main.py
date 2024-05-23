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
from menu import Button, Menu, Text
from CONSTS import FRAMERATE, WINDOW_SIZE, GAME_NAME, PLAYERS, SPAWNABLE_X, COLORS, DEBUG
from physics import move_entities, def_map
from weapon import Bazooka, Sniper, Grenade, GrenadeFrag, Fleche, ChargeBar
from random import randint, choice
from math import pi
from utils import get_circle
from worms import Worm


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_NAME)

        # flags = pygame.FULLSCREEN | pygame.HWSURFACE
        self.SCREEN = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))  # , flags)
        self.active_menu: Menu = Menu("Loading", WINDOW_SIZE[0], WINDOW_SIZE[1],
                                      pygame.image.load("assets/textures/menu/backgrounds/loading.png").convert_alpha())
        self.active_menu.draw(self.SCREEN)
        pygame.display.flip()

        self.path = "assets/map/01.map"
        self.map = TileMap(self.path)
        def_map(self.map)

        self.Oclock = pygame.time.Clock()
        self.tick = 0
        self.fps = 0

        self.map.blit_texture(all_pxs=True)

        self.all_sprites: set[Entity] = set()

        self.current_player = None
        self.players: list[Worm] = []

        self.running = False
        self.pause = False

        self.charg_bar = ChargeBar(self, (self.map.dimensions[0] // 2) - 30, (self.map.dimensions[1] // 2) - 60)
        self.fleche = Fleche(self, (self.map.dimensions[0] // 2) - 25, (self.map.dimensions[1] // 2) - 20,
                             "assets/textures/weapons/arrow.png", 0, 50)
        self.current_weapon = -1
        self.weapon = None
        self.inclinaison = 0.0

        self.MAIN_MENU = None
        self.PAUSE_MENU = None
        self.END_MENU = None
        self.load_menus()
        self.generate_players()

    def generate_players(self):
        for i in range(PLAYERS):
            sp = choice(SPAWNABLE_X)
            x = randint(sp[0], sp[1])
            self.players.append(Worm(self, COLORS[i % 12], x, 0))
        self.current_player = 0

    def load_menus(self):
        title_font = pygame.font.SysFont("Showcard Gothic", 120, False, False)
        small_title_font = pygame.font.SysFont("Showcard Gothic", 80, False, False)

        resume_button = Button(self.SCREEN.get_width() // 2 - 105, self.SCREEN.get_height() // 2 - 44 - 100,
                               pygame.image.load("assets/textures/menu/buttons/resume.png").convert_alpha(), 1,
                               self.exit_menu)
        options_button = Button(self.SCREEN.get_width() // 2 - 105, self.SCREEN.get_height() // 2 - 44,
                                pygame.image.load("assets/textures/menu/buttons/options.png").convert_alpha(), 1, None)
        quit_button = Button(self.SCREEN.get_width() // 2 - 105, self.SCREEN.get_height() // 2 - 44 + 100,
                             pygame.image.load("assets/textures/menu/buttons/quit.png").convert_alpha(), 1,
                             self.exit_game)
        play_button = Button(self.SCREEN.get_width() // 2 - 210, self.SCREEN.get_height() // 2 - 44 + 200,
                             pygame.image.load("assets/textures/menu/buttons/play.png").convert_alpha(), 2,
                             self.exit_menu)
        pause_text = Text(self.SCREEN.get_width() // 2 - 125, self.SCREEN.get_height() // 2 - 250, "Pause",
                          small_title_font, True)
        title_text = Text(self.SCREEN.get_width() // 2 - 300, self.SCREEN.get_height() // 2 - 350, GAME_NAME,
                          title_font, True)

        self.PAUSE_MENU = Menu("Pause", WINDOW_SIZE[0], WINDOW_SIZE[1],
                               pygame.image.load("assets/textures/menu/backgrounds/pause.png").convert_alpha(),
                               [resume_button, options_button, quit_button], [pause_text])
        self.MAIN_MENU = Menu("Main", WINDOW_SIZE[0], WINDOW_SIZE[1],
                              pygame.image.load("assets/textures/menu/backgrounds/main.png").convert_alpha(),
                              [play_button, options_button, quit_button], [title_text])
        self.END_MENU = Menu("Fin", WINDOW_SIZE[0], WINDOW_SIZE[1],
                             pygame.image.load("assets/textures/menu/backgrounds/end.png").convert_alpha(), [], [])

    def exit_game(self):
        self.running = False

    def set_active_menu(self, menu: Menu):
        self.active_menu = menu
        self.active_menu.draw(self.SCREEN)

    def exit_menu(self):
        self.active_menu = None

    def get_current_player(self) -> Worm:
        return self.players[self.current_player]

    def next_player(self):
        self.current_player += 1
        self.current_player %= len(self.players)

    def next_weapon(self):
        if self.weapon is not None:
            self.weapon.kill()
        self.current_weapon += 1
        self.current_weapon %= 4
        match self.current_weapon:
            case 0:
                self.weapon = Bazooka(self, self.get_current_player().x, self.get_current_player().y,
                                      self.inclinaison)
            case 1:
                self.weapon = Sniper(self, self.get_current_player().x, self.get_current_player().y,
                                     self.inclinaison)
            case 2:
                self.weapon = Grenade(self, self.get_current_player().x, self.get_current_player().y,
                                      self.inclinaison)
            case 3:
                self.weapon = GrenadeFrag(self, self.get_current_player().x, self.get_current_player().y,
                                          self.inclinaison)

    def run(self):
        self.running = True
        self.set_active_menu(self.MAIN_MENU)

        power = 0.1
        get_axis = 0
        self.next_weapon()
        # ----------------- Boucle principale -------------------
        while self.running:
            if self.active_menu is not None:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.active_menu.on_click(pygame.mouse.get_pos())
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DELETE:
                            self.exit_game()
            else:
                self.map.blit_texture()
                self.SCREEN.blit(self.map.Surf, (0, 0))

                # ------------- Gestion des événements -------------------
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DELETE:
                            self.exit_game()
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                            self.set_active_menu(self.PAUSE_MENU)
                        if event.key == pygame.K_e:
                            self.next_weapon()
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            if event.key == pygame.K_DOWN:
                                get_axis = -1
                            else:
                                get_axis = 1
                        if event.key == pygame.K_SPACE:
                            if self.current_weapon == 1 and not self.map[self.weapon.x + 25, self.weapon.y + 25]:
                                self.weapon.shoot(power, self.inclinaison)
                                self.next_player()
                            if self.current_weapon == 0 or self.current_weapon == 2 or self.current_weapon == 3:
                                power = -self.tick * 0.015
                                self.charg_bar.charging = True
                                self.charg_bar.up_taille(10, self.get_current_player().x, self.get_current_player().y)
                        if DEBUG:
                            if event.key == pygame.K_m:
                                self.next_player()
                            if event.key == pygame.K_o:
                                get_time_incache()
                                print("Available :", self.map.available_ONMAPs)
                                print("To clean :", self.map.clear_ONMAPs)

                    if event.type == pygame.KEYUP:
                        self.charg_bar.charging = False
                        if event.key == pygame.K_SPACE:
                            power += self.tick * 0.015 + 0.2
                            if power > 1:
                                power = 1
                            if self.current_weapon in (0, 2, 3) and not self.map[
                                self.weapon.x + 25, self.weapon.y + 25]:
                                self.weapon.shoot(power, self.inclinaison)
                                self.next_player()
                            power = 0.2
                            self.charg_bar.reset_taille()
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            if event.key == pygame.K_DOWN:
                                get_axis = 0
                            else:
                                get_axis = 0
                    if event.type == pygame.MOUSEBUTTONDOWN and DEBUG:
                        print("Mouse point @", pygame.mouse.get_pos())
                        circle = get_circle(5, pos := pygame.mouse.get_pos(), radius := 40)
                        self.map.destruction_stack.append((pygame.mouse.get_pos(), 40.0))
                        self.map.destruction_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
                    if event.type == pygame.QUIT:
                        self.exit_game()

                # ------------- Affichage des Entités --------------------
                for sprite in self.all_sprites:
                    sprite.draw(self.SCREEN)

                # ------------- Gestion des gros joujoux -----------------

                if self.charg_bar.charging:
                    charge = power + self.tick * 0.015 + 0.2
                    if charge < 1:
                        self.charg_bar.up_taille(1.5, self.get_current_player().x, self.get_current_player().y)

                if get_axis != 0:
                    if get_axis == -1:
                        self.inclinaison += 0.030
                    else:
                        self.inclinaison -= 0.030

                self.weapon.move_with_rota(self.inclinaison, self.get_current_player().x, self.get_current_player().y)

                self.fleche.move_with_rota(self.inclinaison, self.get_current_player().x, self.get_current_player().y)
                self.charg_bar.moove_bar(self.get_current_player().x, self.get_current_player().y)

                # ------------- Execution des explosions -----------------

                self.map.void_destruction_stack()

                # ------------- Déplacement des Entités ------------------

                move_entities()

                # ---------------------- Fin du jeu ----------------------
                if len(self.players) <= 1:
                    self.set_active_menu(self.END_MENU)

                # ------------- Mouvement des joueurs --------------------
                x_movement = 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    x_movement = -2
                if keys[pygame.K_d]:
                    x_movement = 2
                self.get_current_player().move_worm(x_movement, 0, self.map.map)
                if keys[pygame.K_z]:
                    self.players[self.current_player].jump_worm(self.tick, self.map.map)
                for i in range(len(self.players)):
                    if i != self.current_player:
                        self.players[i].move_worm(0, 0, self.map.map)

                # self.get_current_player().draw(SCREEN)

                # -------------- Actualisation pygame --------------------
                self.Oclock.tick(FRAMERATE)
                self.tick += 1
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    theGame = Game()
    theGame.run()
