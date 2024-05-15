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
from CONSTS import FRAMERATE, WINDOW_SIZE, GAME_NAME
from physics import move_entities, addtomove, def_map
from weapon import ProBazooka, Bazooka, ProSniper, ProGrenade, ProFragGrenade, ChargeBar, Sniper, Grenade, \
    GrenadeFrag, Fleche
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
                                      pygame.image.load("assets/menu/backgrounds/loading.png").convert_alpha())
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

        self.current_player = 0
        self.players: list[Worm] = [Worm(0, 680, 358), Worm(0, 1300, 358)]

        self.running = False
        self.pause = False

        self.MAIN_MENU = None
        self.PAUSE_MENU = None
        self.END_MENU = None
        self.load_menus()

    def load_menus(self):
        title_font = pygame.font.SysFont("Showcard Gothic", 120, False, False)
        small_title_font = pygame.font.SysFont("Showcard Gothic", 80, False, False)

        resume_button = Button(self.SCREEN.get_width() // 2 - 105, self.SCREEN.get_height() // 2 - 44 - 100,
                               pygame.image.load("assets/menu/buttons/resume.png").convert_alpha(), 1, self.exit_menu)
        options_button = Button(self.SCREEN.get_width() // 2 - 105, self.SCREEN.get_height() // 2 - 44,
                                pygame.image.load("assets/menu/buttons/options.png").convert_alpha(), 1, None)
        quit_button = Button(self.SCREEN.get_width() // 2 - 105, self.SCREEN.get_height() // 2 - 44 + 100,
                             pygame.image.load("assets/menu/buttons/quit.png").convert_alpha(), 1, self.exit_game)
        play_button = Button(self.SCREEN.get_width() // 2 - 210, self.SCREEN.get_height() // 2 - 44 + 200,
                             pygame.image.load("assets/menu/buttons/play.png").convert_alpha(), 2, self.exit_menu)
        pause_text = Text(self.SCREEN.get_width() // 2 - 125, self.SCREEN.get_height() // 2 - 250, "Pause",
                          small_title_font, True)
        title_text = Text(self.SCREEN.get_width() // 2 - 300, self.SCREEN.get_height() // 2 - 350, GAME_NAME,
                          title_font, True)

        self.PAUSE_MENU = Menu("Pause", WINDOW_SIZE[0], WINDOW_SIZE[1],
                               pygame.image.load("assets/menu/backgrounds/pause.png").convert_alpha(),
                               [resume_button, options_button, quit_button], [pause_text])
        self.MAIN_MENU = Menu("Main", WINDOW_SIZE[0], WINDOW_SIZE[1],
                              pygame.image.load("assets/menu/backgrounds/main.png").convert_alpha(),
                              [play_button, options_button, quit_button], [title_text])
        self.END_MENU = Menu("Fin", WINDOW_SIZE[0], WINDOW_SIZE[1],
                             pygame.image.load("assets/menu/backgrounds/end.png").convert_alpha(), [], [])

    def exit_game(self):
        self.running = False

    def set_active_menu(self, menu: Menu):
        self.active_menu = menu
        self.active_menu.draw(self.SCREEN)

    def exit_menu(self):
        self.active_menu = None

    def get_current_player(self):
        return self.players[self.current_player]

    def next_player(self):
        self.current_player += 1
        self.current_player %= len(self.players)

    def run(self):
        self.running = True
        self.set_active_menu(self.MAIN_MENU)
        for player in self.players:
            self.all_sprites.add(player)

        # TODO
        actual_weapon = 0
        inclinaison = 0.0
        power = 0.1
        get_axis = 0

        bazooka = Bazooka((self.map.dimensions[0] // 2) - 25, (self.map.dimensions[1] // 2) - 25,
                          "assets/textures/Bazooka2.png", 0, -40, 50)
        self.all_sprites.add(bazooka)
        charg_bar = ChargeBar((self.map.dimensions[0] // 2) - 30, (self.map.dimensions[1] // 2) - 60)
        self.all_sprites.add(charg_bar)
        fleche = Fleche((self.map.dimensions[0] // 2) - 25, (self.map.dimensions[1] // 2) - 20,
                        "assets/textures/Fleche.png", 0, 50)
        self.all_sprites.add(fleche)

        # ----------------- Boucle principale -------------------
        while self.running:
            if self.active_menu is not None:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.active_menu.on_click(pygame.mouse.get_pos())
                    # elif event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    #         self.exit_menu()
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
                        elif event.key == pygame.K_DELETE:
                            self.exit_game()
                        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                            self.set_active_menu(self.PAUSE_MENU)
                        elif event.key == pygame.K_e:
                            if actual_weapon <= 2:
                                actual_weapon += 1
                            else:
                                actual_weapon = 0
                            match actual_weapon:
                                case 0:
                                    bazooka = Bazooka((self.map.dimensions[0] // 2) - 25,
                                                      (self.map.dimensions[1] // 2) - 25,
                                                      "assets/textures/Bazooka2.png", -inclinaison * 360 / (2 * pi),
                                                      -40, 50)
                                    bazooka.move_with_rota(inclinaison, self.get_current_player().x, self.get_current_player().y)
                                    self.all_sprites.add(bazooka)
                                    grenade_frag.kill()
                                case 1:
                                    sniper = Sniper((self.map.dimensions[0] // 2) - 25,
                                                    (self.map.dimensions[1] // 2) - 25,
                                                    "assets/textures/Sniper.png", -inclinaison * 360 / (2 * pi), 0, 50)
                                    sniper.move_with_rota(inclinaison, self.get_current_player().x, self.get_current_player().y)
                                    self.all_sprites.add(sniper)
                                    bazooka.kill()
                                case 2:
                                    grenade = Grenade((self.map.dimensions[0] // 2) - 25,
                                                      (self.map.dimensions[1] // 2) - 25,
                                                      "assets/textures/Grenade.png", -inclinaison * 360 / (2 * pi), 0,
                                                      50)
                                    grenade.move_with_rota(inclinaison, self.get_current_player().x, self.get_current_player().y)
                                    self.all_sprites.add(grenade)
                                    sniper.kill()
                                case 3:
                                    grenade_frag = GrenadeFrag((self.map.dimensions[0] // 2) - 25,
                                                               (self.map.dimensions[1] // 2) - 25,
                                                                "assets/textures/Grenade_frag.png",
                                                               -inclinaison * 360 / (2 * pi), 0, 50)
                                    grenade_frag.move_with_rota(inclinaison, self.get_current_player().x, self.get_current_player().y)
                                    self.all_sprites.add(grenade_frag)
                                    grenade.kill()
                                # elif event.key == pygame.K_f:
                                #    self.map = TileMap(self.path)
                                #    self.map.blit_texture(all_pxs=True)
                        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            if event.key == pygame.K_DOWN:
                                get_axis = -1
                            else:
                                get_axis = 1
                        elif event.key == pygame.K_SPACE:
                            if actual_weapon == 1:
                                pro_sniper = ProSniper(int(round(sniper.x + 25)), int(round(sniper.y + 25)),
                                                        "assets/textures/Explosion.png", self.map.destruction_stack,
                                                       120, 8,
                                                       False)
                                self.all_sprites.add(pro_sniper)
                                addtomove(power * pro_sniper.speed, inclinaison, pro_sniper, pro_sniper.destroy)
                                pro_sniper.launched = True
                                print("missile launched")
                            if actual_weapon == 0 or actual_weapon == 2 or actual_weapon == 3:
                                power = -self.tick * 0.015
                                charg_bar.agrandissement = True
                                charge = power
                                charg_bar.up_taille(10, self.get_current_player().x, self.get_current_player().y)
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            power += self.tick * 0.015 + 0.2
                            if power > 1:
                                power = 1
                            if actual_weapon == 0:
                                pro_bazooka = ProBazooka(int(round(bazooka.x + 25)), int(round(bazooka.y + 25)),
                                                          "assets/textures/Explosion.png", self.map.destruction_stack,
                                                         12,
                                                         25, False)
                                self.all_sprites.add(pro_bazooka)
                                addtomove(power * pro_bazooka.speed, inclinaison, pro_bazooka, pro_bazooka.destroy)
                                pro_bazooka.launched = True
                            elif actual_weapon == 2:
                                pro_grenade = ProGrenade(int(round(grenade.x + 25)), int(round(grenade.y + 25)),
                                                          "assets/textures/Grenade.png", self.map.destruction_stack, 7,
                                                         20,
                                                         True)
                                self.all_sprites.add(pro_grenade)
                                addtomove(power * pro_grenade.speed, inclinaison, pro_grenade, pro_grenade.destroy)
                                pro_grenade.launched = True
                            elif actual_weapon == 3:
                                pro_frag_grenade = ProFragGrenade(int(round(grenade_frag.x + 25)),
                                                                  int(round(grenade_frag.y + 25)),
                                                                    "assets/textures/Grenade_frag.png",
                                                                  self.map.destruction_stack, 7, 20, True)
                                self.all_sprites.add(pro_frag_grenade)
                                addtomove(power * pro_frag_grenade.speed, inclinaison, pro_frag_grenade,
                                          pro_frag_grenade.destroy)
                                pro_frag_grenade.launched = True
                            power = 0.2
                            print("missile launched")
                            charg_bar.agrandissement = False
                            charg_bar.reset_taille()

                        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            if event.key == pygame.K_DOWN:
                                get_axis = 0
                            else:
                                get_axis = 0
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        print("Mouse point @", pygame.mouse.get_pos())
                        circle = get_circle(5, pos := pygame.mouse.get_pos(), radius := 40)
                        self.map.destruction_stack.append((pygame.mouse.get_pos(), 40.0))
                        self.map.destruction_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
                    elif event.type == pygame.QUIT:
                        self.exit_game()

                # ------------- Affichage des Entités --------------------
                for sprite in self.all_sprites:
                    self.SCREEN.blit(sprite.image, (sprite.x - sprite.offset_x, sprite.y - sprite.offset_y))

                if charg_bar.agrandissement:
                    charge = power + self.tick * 0.015 + 0.2
                    if charge < 1:
                        charg_bar.up_taille(1.5, self.get_current_player().x, self.get_current_player().y)

                # ------------- Execution des explosions -----------------

                if get_axis != 0:
                    if get_axis == -1:
                        inclinaison += 0.015
                    else:
                        inclinaison -= 0.015
                match actual_weapon:
                    case 0:
                        bazooka.rotate(-inclinaison * 360 / (2 * pi))
                        bazooka.move_with_rota(inclinaison, self.get_current_player().x, self.get_current_player().y)
                    case 1:
                        sniper.rotate(-inclinaison * 360 / (2 * pi))
                        sniper.move_with_rota(inclinaison, self.get_current_player().x, self.get_current_player().y)
                    case 2:
                        grenade.rotate(-inclinaison * 360 / (2 * pi))
                        grenade.move_with_rota(inclinaison, self.get_current_player().x, self.get_current_player().y)
                    case 3:
                        grenade_frag.rotate(-inclinaison * 360 / (2 * pi))
                        grenade_frag.move_with_rota(inclinaison, self.get_current_player().x, self.get_current_player().y)
                fleche.rotate(-inclinaison * 360 / (2 * pi))
                fleche.move_with_rota(inclinaison, self.get_current_player().x, self.get_current_player().y)
                charg_bar.moove_bar(self.get_current_player().x, self.get_current_player().y)

                self.map.void_destruction_stack()

                # ------------- Déplacement des Entités ------------------
                move_entities()

                # ------------- Mouvement des joueurs --------------------
                x_movement = 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    x_movement = -2
                if keys[pygame.K_d]:
                    x_movement = 2
                self.players[self.current_player].move_worm(x_movement, 0, self.map.map)
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
