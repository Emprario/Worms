"""
Map management
La méthode de gestion des maps reste à déterminer
    - Comment la charger depuis un fichier externe (assets/map/??.map)
    - Comment représenter dans le programme de la matière
"""
import pygame

from CONSTS import MAP_KEYWORD, DEFAULT_DENSITY, coordinate
from physics import get_circle, is_inner_point
from weapons import Weapon


class Map:
    """Représentation de la Map sous forme d'un objet"""

    def __init__(self, mappath: str, surface: pygame.Surface):
        """Chargement de la map dans un objet (chargement logique)."""
        self.map: list[list[coordinate]] = []
        with open(mappath, "r") as file:
            for line in file:
                if line == MAP_KEYWORD + '\n':
                    self.map.append([])
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

        self.polygones: list[pygame.Rect] = []
        self.SURFACE: pygame.Surface = surface
        self.combinatoire: dict[pygame.Rect, list[coordinate]] = {}
        self.create_polygones()

    def destroy_map(self, impact: coordinate, weapon: Weapon):
        """
        Enregistre une destruction de la map, utilise un point d'impact et une arme caractéristique ansi qu'une puissance
        :param impact: Position (x, y)
        :param weapon: Arme utilisée
        """
        # Step 1 : Draw a circle
        circle = get_circle(DEFAULT_DENSITY, impact, weapon.power)

        # Step 2 : Get sequences of inner point
        inners: dict[tuple[coordinate], list[list[coordinate]]] = {}
        for polygone in self.map:
            for point in circle:
                if is_inner_point(point, polygone):
                    if tuple(polygone) in inners:
                        inners[tuple(polygone)][-1].append(point)
                    else:
                        inners[tuple(polygone)] = [[point]]
                else:
                    if polygone in inners:
                        inners[tuple(polygone)].append([])

        # Step 3 : contact points association
        startpoints = {}  # Dict seq of points -> contact point
        for tppolygone in inners.keys():
            # Get the points destroyed : Predecessor
            for i in range(len(inners[tppolygone])):
                j = 0
                while len(tppolygone) == j and is_inner_point(tppolygone[j], circle):
                    startpoints[tuple(inners[tppolygone][i])] = tppolygone[j - 1]
                    j += 1
                    break
                else:
                    # if j >= len(tppolygone)-2:  # Every point are destroyed except 1 of them
                    ...

        # Step 4 : Delete every over point inside the circle
        i = 0
        while i < len(self.map):
            j = 0
            form = self.map[i]
            while j < len(form):
                if is_inner_point((form[j][0], form[j][1]), circle):
                    del form[j]
                else:
                    j += 1
                # On ne peut pas dessiner de polygone à moins de 3 côtés
                # if len(form) < 3:
                #    del self.map[i]

        # Step 5 : Insert new points to self.map
        ...

    def create_polygones(self):
        """ Création de la map polygonale """
        for points in self.map:
            rect = pygame.draw.polygon(self.SURFACE, "white", points)
            self.polygones.append(rect)
            self.combinatoire[rect] = points

    def print_map(self):
        """Chargerment des images en mémoire pour affichage."""
        pass


class TriPixel:
    """Element de base de la Map"""

    def __init__(self, base_texture: str):
        """
        Chargement du Triangle Rectangle Pixel
        :param base_texture: Chemin vers la texture de base du pixel
        """
        pass

    def update_decoration(self):
        """Se met à jour pour ajouter des textures supplémentaires au pixel"""
        pass

    def pg_flip(self):
        """Pygame Filp : Fonction d'update spécifique au TriPixel"""
        pass


if __name__ == "__main__":
    print("Suite de test.")
    mapobj = Map("./assets/map/dummy.map")
    print(mapobj.map)
    print(list(get_circle(DEFAULT_DENSITY, (0, 0), 10)))
