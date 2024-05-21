from __future__ import annotations
from typing import TYPE_CHECKING

from physics import addtomove

if TYPE_CHECKING:
    from main import Game

import pygame

from entity import Entity
from math import sin, cos, pi
from utils import get_circle
from CONSTS import coordinate, COEF_DIST_DAMAGE


class Fleche(Entity):
    def __init__(self, game: Game, x: int, y: int, image: str, angle: int, size: int):
        super().__init__(game, x, y)
        self.original = pygame.image.load(image)
        self.x_base = self.x
        self.y_base = self.y
        self.angle = angle
        self.original = pygame.transform.scale(self.original, (size, size))
        self.image = pygame.transform.rotate(self.original, angle)

    def move_with_rota(self, angle, x, y):
        self.x_base = x - 15
        self.y_base = y - 50
        self.rx = self.x_base + cos(angle) * 120
        self.ry = self.y_base + sin(angle) * 120
        self.image = pygame.transform.rotate(self.original, - (angle * 360 / (2 * pi)) + self.angle)
        self.update_co_from_rco()


# all_moves: list[tuple[float, float, list[list[bool]], coordinate, Entity, bool, int, Callable]] = list()
class ChargeBar(Entity):
    def __init__(self, game: Game, x: int, y: int):
        super().__init__(game, x, y)
        self.image = pygame.Surface((0, 15))
        self.image.fill((255, 0, 0))
        self.taille = 0
        self.charging = False
        self.x_base = self.x
        self.y_base = self.y

    def up_taille(self, vitesse: float, x, y):
        self.taille += vitesse
        self.image = self.image = pygame.Surface((self.taille, 15))
        self.image.fill((255, 0, 0))

    def reset_taille(self):
        self.taille = 0
        self.image = self.image = pygame.Surface((self.taille, 15))

    def moove_bar(self, x, y):
        self.x_base = x
        self.y_base = y
        self.rx = self.x_base - 30
        self.ry = self.y_base - 100
        self.update_co_from_rco()


class Weapon(Entity):
    def __init__(self, game: Game, x: int, y: int, image: str, rotation: float, angle: float, size: int):
        super().__init__(game, x, y)
        self.original = pygame.image.load(image)
        self.angle = angle
        self.original = pygame.transform.scale(self.original, (size, size))
        self.image = pygame.transform.rotate(self.original, angle + rotation)
        self.x_base = self.x
        self.y_base = self.y

    def move_with_rota(self, angle, x, y):
        self.x_base = x - 15
        self.y_base = y - 50
        self.rx = self.x_base + cos(angle) * 60
        self.ry = self.y_base + sin(angle) * 60
        self.image = pygame.transform.rotate(self.original, - (angle * 360 / (2 * pi)) + self.angle)
        self.update_co_from_rco()

    def shoot(self, power, inclinaison):
        pass


class Bazooka(Weapon):
    def __init__(self, game: Game, x: int, y: int, angle: float):
        super().__init__(game, x, y, "assets/textures/Bazooka2.png", 20, angle, 50)

    def shoot(self, power, inclinaison):
        pro_bazooka = ProBazooka(self.game, self.x + 25, self.y + 25)
        print("x: " + str(self.x) + " y: " + str(self.y))
        addtomove(power * pro_bazooka.speed, inclinaison, pro_bazooka, pro_bazooka.destroy, pro_bazooka.kill)


class Sniper(Weapon):
    def __init__(self, game: Game, x: int, y: int, angle: float):
        super().__init__(game, x, y, "assets/textures/Sniper.png", 0, angle, 50)

    def shoot(self, power, inclinaison):
        pro_sniper = ProSniper(self.game, self.x + 25, self.y + 25)
        addtomove(power * pro_sniper.speed, inclinaison, pro_sniper, pro_sniper.destroy, pro_sniper.kill)


class Grenade(Weapon):
    def __init__(self, game: Game, x: int, y: int, angle: float):
        super().__init__(game, x, y, "assets/textures/Grenade.png", 0, angle, 50)

    def shoot(self, power, inclinaison):
        pro_grenade = ProGrenade(self.game, self.x + 25, self.y + 25)
        addtomove(power * pro_grenade.speed, inclinaison, pro_grenade, pro_grenade.destroy, pro_grenade.kill)


class GrenadeFrag(Weapon):
    def __init__(self, game: Game, x: int, y: int, angle: float):
        super().__init__(game, x, y, "assets/textures/Grenade_frag.png", 0, angle, 50)

    def shoot(self, power, inclinaison):
        pro_grenade_frag = ProFragGrenade(self.game, self.x + 25, self.y + 25)
        addtomove(power * pro_grenade_frag.speed, inclinaison, pro_grenade_frag, pro_grenade_frag.destroy,
                  pro_grenade_frag.kill)


class Projectile(Entity):
    def __init__(self, game: Game, x: int, y: int, image: str, speed: float, taille: int, rebond: bool, damage: int):
        super().__init__(game, x, y)
        self.can_bounce = False
        self.image = pygame.Surface((taille, taille))
        self.speed = speed
        self.rebond = rebond
        self.damage = damage
        self.original = pygame.image.load(image)
        self.image = pygame.transform.scale(self.original, (taille, taille))

    def destroy(self, *args):
        self.kill()

    def explosion_damage(self, explosions: list[tuple[coordinate, float, float]]):
        """
        :param explosions: Tuple[center, radius]
        """
        for center, radius, damage in explosions:
            for player in self.game.players:
                dist = ((player.x - center[0]) ** 2 + (player.y - center[1]) ** 2) ** 0.5
                if dist < radius:
                    player.hit(damage * (dist / radius))


class ProBazooka(Projectile):
    def __init__(self, game: Game, x: int, y: int):
        super().__init__(game, x, y, "assets/textures/Explosion.png", 12, 25, False, 10)

    def destroy(self, *args):
        if not args[-1]:
            self.game.map.destruction_stack.append(((self.x, self.y), 50))
            self.explosion_damage([((self.x, self.y), 50, self.damage)])
            super().destroy()


class ProSniper(Projectile):
    def __init__(self, game: Game, x: int, y: int):
        super().__init__(game, x, y, "assets/textures/Explosion.png", 120, 8, False, 10)

    def destroy(self, *args):
        if not args[-1]:
            self.game.map.destruction_stack.append(((self.x, self.y), 10))
            self.explosion_damage([((self.x, self.y), 10, self.damage)])
            super().destroy()


class ProGrenade(Projectile):
    def __init__(self, game: Game, x: int, y: int):
        super().__init__(game, x, y, "assets/textures/Grenade.png", 7, 20, True, 10)
        self.can_bounce = True

    def destroy(self, *args):
        if not args[-1]:
            self.game.map.destruction_stack.append(((self.x, self.y), 60))
            self.explosion_damage([((self.x, self.y), 60, self.damage)])
            super().destroy()


class ProFragGrenade(Projectile):
    def __init__(self, game: Game, x: int, y: int):
        super().__init__(game, x, y, "assets/textures/Grenade_frag.png", 7, 20, True, 10)
        self.can_bounce = True

    def destroy(self, *args):
        if not args[-1]:
            circle = get_circle(5, pos := (self.x, self.y), radius := 50)
            self.game.map.destruction_stack.append((pos, 50))
            self.game.map.destruction_stack.extend([(circle[i], 30.0) for i in range(len(circle))])
            self.explosion_damage([(circle[i], 30.0, self.damage) for i in range(len(circle))] + [(pos, 50, self.damage)])
            super().destroy()
