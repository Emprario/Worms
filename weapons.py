"""Weapons management"""


class Weapon:
    """Arme générique"""

    def __init__(self, texture: str):
        """
        Constructeur ...
        :param texture: Chemin vers la texture
        """
        self.power = 10

    def pg_flip(self):
        """Pygame Filp : Fonction d'update spécifique au worm"""
        pass


class StGrenade(Weapon):
    """Exemple d'objet spécifique : la St Grenade"""
    pass
