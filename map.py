"""
Map management
La méthode de gestion des maps reste à déterminer
    - Comment la charger depuis un fichier externe (assets/map/??.map)
    - Comment représenter dans le programme de la matière
"""
import pygame

from CONSTS import MAP_KEYWORD_REGISTRATION, MAP_KEYWORD_TEXTURE, DEFAULT_DENSITY, coordinate
from physics import get_circle, is_inner_point
from weapons import Weapon
from debug import *


class Map:
    """Représentation de la Map sous forme d'un objet"""

    def __init__(self, mappath: str, surface: pygame.Surface):
        """Chargement de la map dans un objet (chargement logique)."""
        self.map: list[list[coordinate]] = []
        self.texture: str = ''
        register_texture = False
        with open(mappath, "r") as file:
            for line in file:
                if register_texture:
                    self.texture = line[:-1]
                elif line == MAP_KEYWORD_REGISTRATION + '\n':
                    self.map.append([])
                elif line == MAP_KEYWORD_TEXTURE + '\n':
                    register_texture = True
                elif line == '\n':
                    continue
                else:
                    try:
                        spline = line.split()
                        if int(spline[0]) < 0 or int(spline[1]) < 0:
                            raise ValueError
                        self.map[-1].append((int(spline[0]), int(spline[1])))
                    except (ValueError, IndexError):
                        if len(line) > 0 and line[-1] == '\n':
                            line = line[:-1]
                        else:
                            line = line
                        raise ValueError(
                            f"Le valeur de '{line}' ne peut être convertie en coordonnée, est-il bien composer de deux"
                            f" entiers positif ?"
                        )
        for i in range(len(self.map)):
            if len(self.map[i]) < 3:
                raise ValueError(f'Map {i + 1} incomplète est composé que de {len(self.map[i])} éléments')

        self.SURFACE: pygame.Surface = surface
        # self.create_polygones()

    def destroy_map(self, impact: coordinate, weapon: Weapon):
        """
        Enregistre une destruction de la map, utilise un point d'impact et une arme caractéristique ansi qu'une puissance
        :param impact: Position (x, y)
        :param weapon: Arme utilisée
        """
        # Step 1 : Draw a circle
        circle = get_circle(DEFAULT_DENSITY, impact, weapon.power)

        # Step 2 : Get sequences of inner point
        inners: dict[int, list[list[coordinate]]] = {}  # Index <- seq of points
        for i in range(len(self.map)):
            for point in circle:
                if is_inner_point(point, self.map[i]):
                    if i in inners:
                        inners[i][-1].append(point)
                    else:
                        inners[i] = [[point]]
                # else:
                #    if i in inners:
                #        inners[i].append([])

        # Step 3 : contact points association + add point to self.map
        registered_predecessors: list[coordinate] = []
        # Parcours à la fois les listes à insérer et lindex du polygone dans self.map
        for idx, seq in inners.items():
            pointer = 0
            id_seq = 0
            registration = False

            # Cherche tant qu'on n'a pas fait toutes les séquences
            while id_seq < len(seq) and pointer < len(self.map[idx]):

                # Check si un point d'origine est blown
                if (is_inner_point(self.map[idx][pointer], circle) and
                        self.map[idx][pointer - 1] not in registered_predecessors):
                    # en def un prédécesseur
                    registered_predecessors.append(self.map[idx][pointer - 1])
                    registration = True

                # Si on vient d'en trouver un, on enregistre les points et ajuste les suites
                if registration:
                    for insertion in range(len(seq[id_seq])):
                        self.map[idx].insert(pointer, seq[id_seq][insertion])
                    pointer += len(seq[id_seq])
                    id_seq += 1
                    registration = False
                else:
                    pointer += 1
            if id_seq < len(seq) and pointer == len(self.map[idx]):
                raise AssertionError("Shouldn't be here !!")

        # Step 4 : Delete every over point inside the circle Except newly incerted ones
        i = 0
        while i < len(self.map):
            j = 0
            form = self.map[i]
            # print(form)
            while j < len(form):
                # print((form[j][0], form[j][1]), " <-in?->", is_inner_point((form[j][0], form[j][1]), circle),
                #      "&& not part of circle ?", (form[j][0], form[j][1]) not in circle)
                if (form[j][0], form[j][1]) not in circle and is_inner_point((form[j][0], form[j][1]), circle):
                    # print("Deleting :", i, j)
                    del self.map[i][j]
                else:
                    j += 1
            # On ne peut pas dessiner de polygone à moins de 3 côtés
            if len(form) < 3:
                del self.map[i]
            else:
                i += 1

    # def create_polygones(self):
    #    """ Création de la map polygonale """
    #    for points in self.map:
    #        pygame.draw.polygon(self.SURFACE, "white", points)

    def print_map(self, surface: pygame.Surface, highlight_points: bool = False):
        """
        Chargerment de la map avec des couleurs vives, les points peuvent être affichés ! (Débogage)
        :param surface: surface sur lequel afficher
        :param highlight_points: Permet d'afficher les points
        """
        for points in self.map:
            pygame.draw.polygon(self.SURFACE, "darkblue", points)
        if highlight_points:
            for points in self.map:
                for point in points:
                    pygame.draw.circle(self.SURFACE, (0, 255, 0), point, 5)

    def pg_blit(self, surface: pygame.Surface):
        """Pygame Blit : Fonction d'affichage spécifique à la map"""
        pass


if __name__ == "__main__":
    mapobj = Map("./assets/map/dummy.map", DEBUG_SCREEN)

    run = True
    while run:
        # print(pygame.mouse.get_pos())
        clear_screen()
        mapobj.print_map(True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                mapobj.destroy_map((490, 157), Weapon(None))
