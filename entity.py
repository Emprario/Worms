import pygame

from math import cos, sin
from CONSTS import G


class Entity(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int):  # , map: list[list[bool]]):
        super().__init__()
        self.rx: float = x
        self.ry: float = y
        self.x: int = x
        self.y: int = y
        # if map[self.x][self.y]:
        #    raise AssertionError("The worms is not supposed to be in a wall")

    def update_co_from_rco(self):
        self.x, self.y = int(round(self.rx)), int(round(self.ry))

    def move_to(self, t, v0, alpha, X0, Y0):
        self.ry, self.rx = (1 / 2) * G * (t ** 2) + v0 * sin(alpha) * t + Y0, v0 * cos(alpha) * t + X0
        self.update_co_from_rco()

    def get_speed(self, t, v0, alpha):
        return G * t + v0 * sin(alpha), v0 * cos(alpha)
