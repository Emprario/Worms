import pygame

from entity import Entity
from math import pi
from math import sin
from math import cos
from utils import get_circle


class Fleche(Entity):
    def __init__(self, x: int, y: int, image: str, angle:int,  size: int):
        super().__init__(x, y)
        self.original = pygame.image.load(image)
        self.x_base=self.x
        self.y_base=self.y
        self.angle= angle
        self.original = pygame.transform.scale(self.original, (size, size))
        self.image = pygame.transform.rotate(self.original, angle)
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original, angle+self.angle)
    def move_with_rota(self,angle):
        self.x=self.x_base+cos(angle)*100
        self.y=self.y_base+sin(angle)*100



# all_moves: list[tuple[float, float, list[list[bool]], coordinate, Entity, bool, int, Callable]] = list()
class Charg_bar(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.image = pygame.Surface((0, 15))
        self.image.fill((255, 0, 0))
        self.taille = 0
        self.agrandissement=False
    def up_taille(self,vitesse: int):
        self.taille += vitesse
        self.image = self.image = pygame.Surface((self.taille, 15))

        self.image.fill((255, 0, 0))
    def reset_taille(self):
        self.taille=0
        self.image = self.image = pygame.Surface((self.taille, 15))


class Weapon(Entity):
    def __init__(self, x: int, y: int, image: str, rotation: int, angle:int,  size: int):
        super().__init__(x, y)
        self.original = pygame.image.load(image)
        self.angle= angle
        self.original = pygame.transform.scale(self.original, (size, size))
        self.image = pygame.transform.rotate(self.original, angle+rotation)
        self.x_base=self.x
        self.y_base=self.y

class Bazooka(Weapon):
    def __init__(self, x: int, y: int, image: str, rotation: int, angle:int,  size: int):
        super().__init__(x, y, image, rotation, angle, size)
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original, angle+self.angle)
    def move_with_rota(self,angle):
        self.x=self.x_base+cos(angle)*20
        self.y=self.y_base+sin(angle)*20


class Sniper(Weapon):
    def __init__(self, x: int, y: int, image: str, rotation: int, angle:int,  size: int):
        super().__init__(x, y, image, rotation, angle, size)
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original, angle+self.angle)
    def move_with_rota(self,angle):
        self.x=self.x_base+cos(angle)*20
        self.y=self.y_base+sin(angle)*20


class Grenade(Weapon):
    def __init__(self, x: int, y: int, image: str, rotation: int, angle:int,  size: int):
        super().__init__(x, y, image, rotation, angle, size)
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original, angle+self.angle)
    def move_with_rota(self,angle):
        self.x=self.x_base+cos(angle)*20
        self.y=self.y_base+sin(angle)*20

class Grenade_frag(Weapon):
    def __init__(self, x: int, y: int, image: str, rotation: int, angle:int,  size: int):
        super().__init__(x, y, image, rotation, angle, size)
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original, angle+self.angle)
    def move_with_rota(self,angle):
        self.x=self.x_base+cos(angle)*20
        self.y=self.y_base+sin(angle)*20
<<<<<<< HEAD

=======
>>>>>>> 00a02e0b4971eb669f34031ef6b17c8cecb7f171


class Projectile(Entity):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack, speed: float,taille: int, rebond: bool):
        super().__init__(x, y)
        self.image = pygame.Surface((taille, taille))
        self.speed = speed
        self.launched = False
        self.map_destroy_stack = map_destroy_stack
        self.rebond = False
        self.original = pygame.image.load(image)
        self.image = pygame.transform.scale(self.original, (taille, taille))


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