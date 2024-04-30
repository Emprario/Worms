import pygame
from entity import Entity
from math import pi
from physics import addtomove

"""Il faut changer l'apel de moveworms dans main, appel de la fonction à chaque frame"""


class Worm(Entity):
    """Classe du ver de terre"""

    def __init__(self, camp: int, x: int, y: int, hp=100):
        """
        Constructeur de Worm
        :param camp: Camp du worm (pas nécessairement binaire)
        """
        super().__init__(x, y)
        self.team = camp # L'équipe du worm
        self.health = hp
        self.alive = True # Checker si le worm est en vie
        self.is_jumping = False # Checker si le joueur saute
        self.is_on_ground = True
        self.jump_current = 0 # Track la hauteur d'un saut actuel, commence = 0 puis < 0 lorsque hauteur maxi atteint
        self.jump_height = 80 # La hauteur maximale d'un saut
        self.movement_distance = 200 # NOT THE FINAL VALUE SUBJECT TO CHANGE
        self.movement_speed = 40 # SUBJECT TO CHANGE
        self.image = pygame.image.load("assets/worm/worm_sprite.png").convert_alpha()

    def drop_worm(self, map, movelst):
        """

        """
        # movelst.append([40, -10, map, (self.x, self.y), self, True, 0])




    def move_worm(self, x_axis, y_axis, map, all_moves, tick):
        """
        Permet de déplacer le worm dans les deux directions
        :param x_axis: Type(int) gauche à droite
        :param y_axis: Type(int) haut à bas
        """

        if self.is_on_ground:

            self.x += x_axis


            # mvt vers le bas
            if not map[self.x][self.y+1]:
                self.y += 2
                for i in range(self.y, len(map[0])):
                    if map[self.x][i]:
                        break
                print(abs(self.y-i))

                #--------------
                if abs(self.y-i) > 30:
                    # def translation(v_init: float, alpha: float, map: list[list[bool]], point0: coordinate, entity: Entity,
                    #             force: bool, local_tick: int) -> tuple[bool, bool, None | float]:
                    #
                    # all_moves: list[list[float, float, list[list[bool]], coordinate, Entity, bool, int, Callable]] = list()
                    addtomove([0, -pi/2, map, self, True, tick, self.fall_damage])
                    self.is_on_ground = False
                #-------------
            # mvt lattéral
            else:
                index = 0
                for i in range(1,len(map[0])):
                    if map[self.x][i] and not map[self.x][i-1]:
                        if abs(i - self.y) < abs(index - self.y):
                            index = i
                if (index-self.y) > -3:
                    self.y += index-self.y

        """ pour le deplacement sur les surface inclinés: prendre la colone
        pixel à droite ou gauch (selon le input), parcourir cet colone pour trouver
        les points de contour (les pixel True apres un false). Ensuite faire la différence
        de y de ces points avec le y du joueur pour trouver le point de contour le plus proche."""



    def jump_worm(self):
        """
        Fait sauter le worm
        :return:
        """
        if self.is_jumping:
            if self.jump_current >= -self.jump_height:  # S'il na pas atteint sa hauteur maximale
                direction = 1  # Le worms monte
                if self.jump_current < 0:
                    direction = -1  # Le worms descend
                self.y -= (self.jump_current ** 2) * 0.5 * direction
                self.jump_current -= 1
            else:
                self.is_jumping = False
                self.jump_current = self.jump_height
                self.is_on_ground = True

    def draw(self, screen):
        screen.blit(self.image, (self.x-62, self.y-80))

    def pg_blit(self, surface: pygame.Surface):
        """Pygame Blit : Fonction d'affichage spécifique au worm"""
        pass

    def fall_damage(self, *args):
        self.is_on_ground = True