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
# RED = (255, 0, 0)

# all_moves: list[tuple[float, float, list[list[bool]], coordinate, Entity, bool, int, Callable]] = list()

class Bazooka(Entity):
    def __init__(self, x: int, y: int, image: str, rotation: int):
        super().__init__(x, y)
        original = pygame.image.load(image)
        resized = pygame.transform.scale(original, (50, 50))
        self.image = pygame.transform.rotate(resized, rotation)
        # self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # self.rect = self.image.get_rect()
        # self.image.blit(rotated_image, self.rect)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        # self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # self.image.blit(image, self.rect)


class Pro_bazooka(Entity):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack):
        super().__init__(x, y)
        self.image = pygame.Surface((20, 20))
        # self.image.blit(pygame.image.load(image), (0, 0))
        # self.rect = self.image.get_rect()
        self.speed = 12
        self.launched = False
        self.map_destroy_stack = map_destroy_stack
        self.rebond = False

    def destroy(self, *args):
        print("blow")
        circle = get_circle(5, pos := (self.x, self.y), radius := 50)
        self.map_destroy_stack.append((pos, 50))
        # self.map_destroy_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
        self.kill()

    # all_moves: list[list[float, float, list[list[bool]], Entity, bool, int, Callable]] = list()
    def add_to_move(self, movelst: list, map: list[list[bool]], tick: int, inclinaison: int, power: int):
        movelst.append([power * self.speed, inclinaison, map, self, True, tick, self.destroy])


class Pro_sniper(Entity):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack):
        super().__init__(x, y)
        self.image = pygame.Surface((7, 7))
        # self.image.blit(pygame.image.load(image), (0, 0))
        # self.rect = self.image.get_rect()
        self.speed = 30
        self.launched = False
        self.map_destroy_stack = map_destroy_stack
        self.rebond = False

    def destroy(self, *args):
        print("blow")
        circle = get_circle(5, pos := (self.x, self.y), radius := 10)
        self.map_destroy_stack.append((pos, 10))
        # self.map_destroy_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
        self.kill()

    # all_moves: list[list[float, float, list[list[bool]], Entity, bool, int, Callable]] = list()
    def add_to_move(self, movelst: list, map: list[list[bool]], tick: int, inclinaison: int, power: int):
        movelst.append([power * self.speed, inclinaison, map, self, True, tick, self.destroy])


class Pro_grenade(Entity):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack):
        super().__init__(x, y)
        self.image = pygame.Surface((8, 8))
        # self.image.blit(pygame.image.load(image), (0, 0))
        # self.rect = self.image.get_rect()
        self.speed = 7
        self.launched = False
        self.map_destroy_stack = map_destroy_stack
        self.rebond = True

    def destroy(self, *args):
        print("blow")
        circle = get_circle(5, pos := (self.x, self.y), radius := 60)
        self.map_destroy_stack.append((pos, 60))
        # self.map_destroy_stack.extend([(circle[i], 20.0) for i in range(len(circle))])
        self.kill()

    # all_moves: list[list[float, float, list[list[bool]], Entity, bool, int, Callable]] = list()
    def add_to_move(self, movelst: list, map: list[list[bool]], tick: int, inclinaison: int, power: int):
        movelst.append([power * self.speed, inclinaison, map, self, True, tick, self.destroy])


class Pro_frag_grenade(Entity):
    def __init__(self, x: int, y: int, image: str, map_destroy_stack):
        super().__init__(x, y)
        self.image = pygame.Surface((9, 9))
        # self.image.blit(pygame.image.load(image), (0, 0))
        # self.rect = self.image.get_rect()
        self.speed = 7
        self.launched = False
        self.map_destroy_stack = map_destroy_stack
        self.rebond = True

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
