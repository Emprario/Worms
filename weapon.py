import pygame

from entity import Entity
from math import pi
from utils import get_circle


# path = "assets/map/01.map"
# map = TileMap(path)

# flags = pygame.FULLSCREEN | pygame.HWSURFACE
# SCREEN = pygame.display.set_mode(map.dimensions, flags)


# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
RED = (255, 0, 0)

# all_moves: list[tuple[float, float, list[list[bool]], coordinate, Entity, bool, int, Callable]] = list()
class Charg_bar(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.image = pygame.Surface((0, 15))
        self.taille = 0
        self.agrandissement=False
    def up_taille(self,vitesse: int):
        self.taille += vitesse
        self.image = self.image = pygame.Surface((self.taille, 30))
    def reset_taille(self):
        self.taille=0
        self.image = self.image = pygame.Surface((self.taille, 30))


class Bazooka(Entity):
    def __init__(self, x: int, y: int, image: str, rotation: int):
        super().__init__(x, y)
        self.original = pygame.image.load(image)
        self.angle= -30
        self.original = pygame.transform.scale(self.original, (50, 50))
        self.image = pygame.transform.rotate(self.original, rotation)

    def rotate(self, angle):
        self.angle += angle
        self.image = pygame.transform.rotate(self.original, self.angle)

class Projectile(Entity):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack, speed: float,taille: int, rebond: bool):
        super().__init__(x, y)
        self.image = pygame.Surface((taille, taille))
        self.speed = speed
        self.launched = False
        self.map_destroy_stack = map_destroy_stack
        self.rebond = False


class Pro_bazooka(Projectile):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack, speed: float,taille: int, rebond: bool):
        super().__init__(x, y, image, map_destroy_stack, speed,taille,rebond)

    def destroy(self, *args):
        print("blow")
        circle = get_circle(5, pos := (self.x, self.y), radius := 50)
        self.map_destroy_stack.append((pos, 50))
        # self.map_destroy_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
        self.kill()


class Pro_sniper(Projectile):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack, speed: float,taille: int, rebond: bool):
        super().__init__(x, y, image, map_destroy_stack, speed,taille,rebond)

    def destroy(self, *args):
        print("blow")
        circle = get_circle(5, pos := (self.x, self.y), radius := 10)
        self.map_destroy_stack.append((pos, 10))
        # self.map_destroy_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
        self.kill()


class Pro_grenade(Projectile):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack, speed: float,taille: int, rebond: bool):
        super().__init__(x, y, image, map_destroy_stack, speed,taille,rebond)

    def destroy(self, *args):
        print("blow")
        circle = get_circle(5, pos := (self.x, self.y), radius := 60)
        self.map_destroy_stack.append((pos, 60))
        # self.map_destroy_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
        self.kill()


class Pro_frag_grenade(Projectile):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack, speed: float,taille: int, rebond: bool):
        super().__init__(x, y, image, map_destroy_stack, speed,taille,rebond)

    def destroy(self, *args):
        print("blow")
        circle = get_circle(5, pos := (self.x, self.y), radius := 50)
        self.map_destroy_stack.append((pos, 50))
        self.map_destroy_stack.extend([(circle[i], 30.0) for i in range(len(circle))])
        self.kill()