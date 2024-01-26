"""
Map management
La méthode de gestion des maps reste à déterminer
    - Comment la charger depuis un fichier externe (assets/map/??.map)
    - Comment représenter dans le programme de la matière
"""
from weapons import Weapon


class Map:
    """Représentation de la Map sous forme d'un objet"""

    def __init__(self, mappath: str):
        """Chargement de la map dans un objet (chargement logique)."""
        pass

    def destroy_map(self, impact: tuple[int, int], weapon: Weapon, power: float):
        """
        Enregistre une destruction de la map, utilise un point d'impact et une arme caractéristique ansi qu'une puissance
        :param impact: Position (x, y)
        :param weapon: Arme utilisée
        :param power: Puissance de l'impact (selon arme)
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
