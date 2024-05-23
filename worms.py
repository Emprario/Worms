from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Game

from math import pi

import pygame

from CONSTS import FALL_LIMIT, AUTO_MOUNT, MIN_SPEED_DAMAGE, JUMP
from entity import Entity
from physics import addtomove

"""Il faut changer l'apel de moveworms dans main, appel de la fonction à chaque frame"""


class Worm(Entity):
    """Classe du ver de terre"""

    def __init__(self, game: Game, color: int, x: int, y: int, hp: float = 100):
        """
        Constructeur de Worm
        :param camp: Camp du worm (pas nécessairement binaire)
        """
        super().__init__(game, x, y, 30, 60)
        self.health = hp
        self.color = color
        self.is_on_ground = True
        # self.inclinaison = 0
        self.current_weapon = -1

        self.face = 0  # face = 1 regard à droite    face = 0 regard à gauche
        self.ChangeFace = False  # Track if the direction of the worms is changed by the movement this frame
        self.image = pygame.image.load("assets/textures/worm/worm.png").convert_alpha()
        scale: float = 0.08
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))

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
                    addtomove(0, -pi / 2, self, self.fall_damage, self.kill)
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
        ite: bool = False
        for p in range(1, AUTO_MOUNT + 1):
            if not map[self.x][self.y - p] and map[self.x][self.y]:
                ite = True

        if ite or not map[self.x][self.y]:
            y_dp = 0
            for i in range(1, len(map[0])):
                if map[self.x][i] and not map[self.x][i - 1] and abs(i - self.y) < abs(y_dp - self.y):
                    y_dp = i
            # print("raw y_dp - self.y:", y_dp - self.y)
            if y_dp - self.y < 0:
                if y_dp - self.y < AUTO_MOUNT:
                    # print("Goes up by", self.y - y_dp)
                    self.y += y_dp - self.y
                else:
                    self.x -= x_axis
            elif y_dp - self.y > 1:
                # print("Goes down by", y_dp - self.y)
                self.y += y_dp - self.y
        else:
            self.x -= x_axis

    def jump_worm(self, tick, map):
        """
        Fait sauter le worm
        :return:
        """
        if self.is_on_ground:
            if self.face == 1:
                addtomove(JUMP, -pi / 3, self, self.fall_damage, self.kill)
            else:
                addtomove(JUMP, -2 * pi / 3, self, self.fall_damage, self.kill)
            self.is_on_ground = False

    def draw(self, screen):
        super().draw(screen)
        font = pygame.font.Font(None, 24)
        hp_surface = font.render(str(round(self.health)), True, (0, 0, 0))
        screen.blit(hp_surface, (self.x - 15, self.y - 80))

        if self.ChangeFace:
            self.image = pygame.transform.flip(self.image, True, False)
            self.ChangeFace = False
        pygame.draw.circle(screen, self.color, (self.x, self.y), radius=5)

    def hit(self, damage: float):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def kill(self, *args):
        super().kill(args)
        for i in range(len(self.game.players)):
            if self.game.players[i] is self:
                self.game.players.pop(i)
                break
        if self.game.current_player == len(self.game.players):
            self.game.current_player = 0

    def fall_damage(self, *args):
        if args[-2] > MIN_SPEED_DAMAGE:
            self.health -= round(2 * args[-2])
        if not args[-1]:
            self.is_on_ground = True
