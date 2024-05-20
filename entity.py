"""
Entitée de la base de pour la gestion du jeux,
    * Elle possède des propriétés élémentaires : des coordonéées réelles et entière
    * Une fonction d'update de coordonées entières à partir des coordonées réelles
    * Des fonctions de déplacements via vecteur vitesse
    * Une fonction pour obtenir la vitesse actuelle
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Game

import pygame

from math import cos, sin
from CONSTS import G


class Entity(pygame.sprite.Sprite):

    def __init__(self, game: Game, x: int, y: int, offset_x: int = 0, offset_y: int = 0):  # , map: list[list[bool]]):
        super().__init__()
        self.game = game
        self.rx: float = x
        self.ry: float = y
        self.x: int = x
        self.y: int = y
        self.offset_x: int = offset_x
        self.offset_y: int = offset_y
        self.game.all_sprites.add(self)
        # if map[self.x][self.y]:
        #    raise AssertionError("The worms is not supposed to be in a wall")

    def update_co_from_rco(self):
        self.x, self.y = int(round(self.rx)), int(round(self.ry))

    def synchroniseXY(self):
        self.rx, self.ry = self.x, self.y

    def move_to(self, t, v0, alpha, mod):
        self.ry += mod * (G * t + v0 * sin(alpha))
        self.rx += mod * v0 * cos(alpha)
        self.update_co_from_rco()

    def get_speed(self, t, v0, alpha):
        return G * t + v0 * sin(alpha), v0 * cos(alpha)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x - self.offset_x, self.y - self.offset_y))

    def kill(self, *args):
        super().kill()
        self.game.all_sprites.remove(self)
        del self

    def __repr__(self) -> str:
        return f"Entity({self.x}, {self.y})"
