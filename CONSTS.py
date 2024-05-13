"""
Module de définitions de constantes élémentaires à travers tout le programme.
Il faut veiller à n'importer aucun module dans celui-ci sauf des modules externes.
Merci de mettre des hints sur les constantes dans le programme afin de faciliter leurs utilisations.
"""


# Errors

class OnLoadMapError(Exception):
    pass


# Constantes

MENU_SIZE = (1920, 1080)
coordinate = tuple[int, int]        # Alias pour les coordonées
DEFAULT_DENSITY = 20                # Densité pour le traçage de cercle
MAX_THREAD_BY_CALC = 1              # Depreceated
SIMULTANITY_THRESHOLD = 256         # Nombre maximum de cache qui est généré
MIN_SIMULTANITY_THRESHOLD = 16      # Nombre minimum de cache pour démarer le programme
G = 0.075                           # G : la constante de gravité
FRAMERATE = 60                      # Le framerate à atteindre (capé)
MILITICK = 50                       # Subdivision du tick pour décomposer le mouvement.
