"""
Module de définitions de constantes élémentaires à travers tout le programme.
Il faut veiller à n'importer aucun module dans celui-ci sauf des modules externes.
Merci de mettre des hints sur les constantes dans le programme afin de faciliter leurs utilisations.
"""


# Errors

class OnLoadMapError(Exception):
    pass


# Constantes

coordinate = tuple[int, int]
DEFAULT_DENSITY = 20
MAX_THREAD_BY_CALC = 1
SIMULTANITY_THRESHOLD = 256
MIN_SIMULTANITY_THRESHOLD = 32
G = 0.075
FRAMERATE = 60
MILITICK = 50