"""
Module de définitions de constantes élémentaires à travers tout le programme.
Il faut veiller à n'importer aucun module dans celui-ci sauf des modules externes.
Merci de mettre des hints sur les constantes dans le programme afin de faciliter leurs utilisations.
"""

VERSION: str = "earlybuilds"

SIZE: tuple[int, int] = (1920, 1080)

MAP_KEYWORD_REGISTRATION: str = "STARTSTOP"
MAP_KEYWORD_TEXTURE: str = "TEXTURE"

DEFAULT_DENSITY: int = 20

# Coordonnée X, Y
coordinate = tuple[int, int]
# Vecteur : Pt d'application, force, angle (rad)
vector = tuple[tuple[int, int], float, float]
