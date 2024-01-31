"""
Map management
La méthode de gestion des maps reste à déterminer
    - Comment la charger depuis un fichier externe (assets/map/??.map)
    - Comment représenter dans le programme de la matière
"""
from CONSTS import MAP_KEYWORD, DEFAULT_DENSITY
from physics import get_circle
from weapons import Weapon
import pygame


class Map:
    """Représentation de la Map sous forme d'un objet"""

    def __init__(self, mappath: str):
        """Chargement de la map dans un objet (chargement logique)."""
        self.map: list[list[tuple[int, int]]] = []
        with open(mappath, "r") as file:
            for line in file:
                if line == MAP_KEYWORD + '\n':
                    self.map.append([])
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

    def destroy_map(self, impact: tuple[int, int], weapon: Weapon):
        """
        Enregistre une destruction de la map, utilise un point d'impact et une arme caractéristique ansi qu'une puissance
        :param impact: Position (x, y)
        :param weapon: Arme utilisée
        """
        pass

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
