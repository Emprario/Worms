import pygame

from entity import Entity
from math import pi
from utils import get_circle
from physics import addtomove


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
        # resized = pygame.transform.scale(self.original, (50, 50))
        self.image = pygame.transform.rotate(self.original, rotation)
        # self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # self.rect = self.image.get_rect(center=(x, y))
        # self.image.blit(rotated_image, self.rect)

    def rotate(self, angle):
        # Rotation de l'image originale pour éviter la dégradation
        self.angle+=angle
        self.image = pygame.transform.rotate(self.original, self.angle)
        # Réajuster le rectangle pour centrer l'image
        # self.rect = self.image.get_rect(center=(self.rect.center))


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
        addtomove([power * self.speed, inclinaison, map, self, True, tick, self.destroy])


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
        addtomove([power * self.speed, inclinaison, map, self, True, tick, self.destroy])


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
        addtomove([power * self.speed, inclinaison, map, self, True, tick, self.destroy])


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
        addtomove([power * self.speed, inclinaison, map, self, True, tick, self.destroy])


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
