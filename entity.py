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

    def move_to(self, t, v0, alpha, mod):
        self.ry += mod * (G * t + v0 * sin(alpha))
        self.rx += mod * v0 * cos(alpha)
        self.update_co_from_rco()

    def get_speed(self, t, v0, alpha):
        return G * t + v0 * sin(alpha), v0 * cos(alpha)
