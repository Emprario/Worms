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



class Projectile(Entity):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack, speed: float,taille: int, rebond: bool):
        super().__init__(x, y)
        self.image = pygame.Surface((taille, taille))
        # self.image.blit(pygame.image.load(image), (0, 0))
        # self.rect = self.image.get_rect()
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

    # all_moves: list[list[float, float, list[list[bool]], Entity, bool, int, Callable]] = list()
    def add_to_move(self, movelst: list, map: list[list[bool]], tick: int, inclinaison: int, power: int):
        movelst.append([power * self.speed, inclinaison, map, self, True, tick, self.destroy])


class Pro_sniper(Projectile):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack, speed: float,taille: int, rebond: bool):
        super().__init__(x, y, image, map_destroy_stack, speed,taille,rebond)

    def destroy(self, *args):
        print("blow")
        circle = get_circle(5, pos := (self.x, self.y), radius := 10)
        self.map_destroy_stack.append((pos, 10))
        # self.map_destroy_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
        self.kill()

    # all_moves: list[list[float, float, list[list[bool]], Entity, bool, int, Callable]] = list()
    def add_to_move(self, movelst: list, map: list[list[bool]], tick: int, inclinaison: int, power: int):
        movelst.append([power * self.speed, inclinaison, map, self, True, tick, self.destroy])


class Pro_grenade(Projectile):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack, speed: float,taille: int, rebond: bool):
        super().__init__(x, y, image, map_destroy_stack, speed,taille,rebond)


    def destroy(self, *args):
        print("blow")
        circle = get_circle(5, pos := (self.x, self.y), radius := 60)
        self.map_destroy_stack.append((pos, 60))
        # self.map_destroy_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
        self.kill()

    # all_moves: list[list[float, float, list[list[bool]], Entity, bool, int, Callable]] = list()
    def add_to_move(self, movelst: list, map: list[list[bool]], tick: int, inclinaison: int, power: int):
        movelst.append([power * self.speed, inclinaison, map, self, True, tick, self.destroy])



class Pro_frag_grenade(Projectile):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack, speed: float,taille: int, rebond: bool):
        super().__init__(x, y, image, map_destroy_stack, speed,taille,rebond)

    def destroy(self, *args):
        print("blow")
        circle = get_circle(5, pos := (self.x, self.y), radius := 50)
        self.map_destroy_stack.append((pos, 50))
        self.map_destroy_stack.extend([(circle[i], 30.0) for i in range(len(circle))])
        self.kill()

    # all_moves: list[list[float, float, list[list[bool]], Entity, bool, int, Callable]] = list()
    def add_to_move(self, movelst: list, map: list[list[bool]], tick: int, inclinaison: int, power: int):
        movelst.append([power * self.speed, inclinaison, map, self, True, tick, self.destroy])


"""    def update(self):
        if self.launched:
            self.rect.x += self.speed
            if self.rect.left > map.dimensions:
                self.kill()"""

"""class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)"""

# Création des obstacles
# obstacle = Obstacle(screen_width - 100, screen_height // 2)
# all_sprites.add(obstacle)
# obstacles.add(obstacle)

"""
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectile = Projectile()
                projectile.rect.center = (50, flags // 2)
                all_sprites.add(projectile)
                projectile.launched = True

    # Vérification des collisions entre projectiles et obstacles
    for projectile in all_sprites:
        if isinstance(projectile, Projectile) and projectile.launched:
            collisions = pygame.sprite.spritecollide(projectile, obstacles, True)
            if collisions:
                projectile.kill()
                
"""

# all_sprites.update()


# screen.fill(BLACK)


# all_sprites.draw(screen)


# pygame.display.flip()


# pygame.time.Clock().tick(60)
