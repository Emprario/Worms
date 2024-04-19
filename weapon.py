import pygame

from entity import Entity
from math import pi

# path = "assets/map/01.map"
# map = TileMap(path)

# flags = pygame.FULLSCREEN | pygame.HWSURFACE
#SCREEN = pygame.display.set_mode(map.dimensions, flags)


# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)

# all_moves: list[tuple[float, float, list[list[bool]], coordinate, Entity, bool, int, Callable]] = list()
class Projectile(Entity):
    def __init__(self, x: int, y: int, image: str):
        super().__init__(x, y)
        self.image = pygame.Surface((10, 10))
        self.image.fill("red")
        # self.rect = self.image.get_rect()
        self.speed = 5
        self.launched = False

    def destroy(self, *args):
        pass

    # all_moves: list[list[float, float, list[list[bool]], Entity, bool, int, Callable]] = list()
    def add_to_move(self, movelst: list, map: list[list[bool]], tick: int):
        movelst.append([50, 0, map, self, True, tick, self.destroy])


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
#obstacle = Obstacle(screen_width - 100, screen_height // 2)
#all_sprites.add(obstacle)
#obstacles.add(obstacle)

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

    
    #all_sprites.update()

    
    #screen.fill(BLACK)

    
    #all_sprites.draw(screen)

    
    #pygame.display.flip()

    
    #pygame.time.Clock().tick(60)



