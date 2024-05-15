from math import pi

import pygame

from CONSTS import FALL_LIMIT, AUTO_MOUNT
from entity import Entity
from physics import addtomove

"""Il faut changer l'apel de moveworms dans main, appel de la fonction à chaque frame"""


class Worm(Entity):
    """Classe du ver de terre"""

    def __init__(self, camp: int, x: int, y: int, hp=100):
        """
        Constructeur de Worm
        :param camp: Camp du worm (pas nécessairement binaire)
        """
        super().__init__(x, y, 62, 60)
        self.team = camp  # L'équipe du worm
        self.health = hp
        self.alive = True  # Checker si le worm est en vie
        self.is_jumping = False  # Checker si le joueur saute
        self.is_on_ground = True
        self.jump_current = 0  # Track la hauteur d'un saut actuel, commence = 0 puis < 0 lorsque hauteur maxi atteint
        self.jump_height = 80  # La hauteur maximale d'un saut
        self.movement_distance = 200  # NOT THE FINAL VALUE SUBJECT TO CHANGE
        self.movement_speed = 40  # SUBJECT TO CHANGE

        self.face = 0  # face = 1 regard à droite    face = 0 regard à gauche
        self.ChangeFace = False  # Track if the direction of the worms is changed by the movement this frame
        self.image = pygame.image.load("assets/worm/sprite.png").convert_alpha()
        scale: float = 0.08
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))


    def drop_worm(self, map, movelst):
        """

        """
        # movelst.append([40, -10, map, (self.x, self.y), self, True, 0])

        
    def move_worm(self, x_axis, y_axis, map):
        """
        Permet de déplacer le worm dans les deux directions
        :param x_axis: Type(int) gauche à droite
        :param y_axis: Type(int) haut à bas
        """

        if self.face == 1 and x_axis < 0:
            self.face = 0
            self.ChangeFace = True
        elif self.face == 0 and x_axis > 0:
            self.face = 1
            self.ChangeFace = True

        if self.is_on_ground:

            self.x += x_axis
            # mvt vers le bas
            if not map[self.x][self.y + 1]:
                # self.y += 2
                for i in range(self.y, len(map[0])):
                    if map[self.x][i]:
                        break

                # --------------
                if abs(self.y - i) > FALL_LIMIT:

                    # def translation(v_init: float, alpha: float, map: list[list[bool]], point0: coordinate, entity: Entity,
                    #             force: bool, local_tick: int) -> tuple[bool, bool, None | float]:
                    #
                    # all_moves: list[list[float, float, list[list[bool]], coordinate, Entity, bool, int, Callable]] = list()
                    addtomove(0, -pi / 2, self, self.fall_damage)
                    self.is_on_ground = False
                # -------------
                else:
                    self.__abs_movement(map, x_axis, y_axis)
            # mvt lattéral
            else:
                self.__abs_movement(map, x_axis, y_axis)


    def __abs_movement(self, map, x_axis, y_axis):
        """ pour le deplacement sur les surface inclinés: prendre la colone
        pixel à droite ou gauche (selon le input), parcourir cet colone pour trouver
        les points de contour (les pixel True apres un false). Ensuite faire la différence
        de y de ces points avec le y du joueur pour trouver le point de contour le plus proche."""
        y_dp = 0
        for i in range(1, len(map[0])):
            if map[self.x][i] and not map[self.x][i - 1] and abs(i - self.y) < abs(y_dp - self.y):
                y_dp = i
        print("raw y_dp - self.y:", y_dp - self.y)
        if y_dp - self.y < 0:
            if y_dp - self.y < AUTO_MOUNT:
                print("Goes up by", self.y - y_dp)
                self.y += y_dp - self.y
            else:
                self.x -= x_axis
        elif y_dp - self.y > 1:
            print("Goes down by", y_dp - self.y)
            self.y += y_dp - self.y

            
    def jump_worm(self, tick, map):
        """
        Fait sauter le worm
        :return:
        """
        if self.is_on_ground:
            if self.face == 1:
                addtomove(2, -pi / 4, self, self.fall_damage)
            else:
                addtomove(2, -3 * pi / 4, self, self.fall_damage)
            self.is_on_ground = False

    def draw(self, screen):
        font = pygame.font.Font(None, 24)
        HP_surface = font.render(str(self.health), True, (0, 0, 0))
        screen.blit(HP_surface, (self.x, self.y - 70))

        if self.ChangeFace:
            self.image = pygame.transform.flip(self.image, True, False)
            self.ChangeFace = False
        screen.blit(self.image, (self.x - 62, self.y - 80))


    def pg_blit(self, surface: pygame.Surface):
        """Pygame Blit : Fonction d'affichage spécifique au worm"""
        pass

      
    def fall_damage(self, *args):
        if args[-1] > 3:
            self.health -= round(2 * args[-1])
        self.is_on_ground = True
