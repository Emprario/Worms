"""
Module de définitions de constantes élémentaires à travers tout le programme.
Il faut veiller à n'importer aucun module dans celui-ci sauf des modules externes.
Merci de mettre des hints sur les constantes dans le programme afin de faciliter leurs utilisations.
"""

from math import pi


# Errors
class OnLoadMapError(Exception):
    pass


# Constantes
GAME_NAME = "PalaVect2"
WINDOW_SIZE = (1920, 1080)
coordinate = tuple[int, int]  # Alias pour les coordonées
DEFAULT_DENSITY = 20  # Densité pour le traçage de cercle
MAX_THREAD_BY_CALC = 1  # Depreceated
SIMULTANITY_THRESHOLD = 32  # Nombre maximum de cache qui est généré
MIN_SIMULTANITY_THRESHOLD = 8  # Nombre minimum de cache pour démarer le programme
G = 0.075  # G : la constante de gravité
FRAMERATE = 60  # Le framerate à atteindre (capé)
MILITICK = 50  # Subdivision du tick pour décomposer le mouvement.
NB_PX_LEFT_RIGHT = 1  # Nb de pixel parcourue à droite et à gauche du pixel d'impact, donne une précision
# Sur la normale de l'impact
SENS_DIRECT = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
# Défini le sens direct (selon l'orientation pygame de l'axe y)
SENS_INDIRECT = SENS_DIRECT[::-1]  # Défini le sens indirect (selon l'orientation pygame de l'axe y)
REMOTE_POINT = 10  # Défini le nombre de point qu'il remonter à l'arrière
MIN_SPEED_BOUNCE = pi  # Défini la speed minimum pour rebondir
BOUNCING = 0.2
FALL_LIMIT = 20
AUTO_MOUNT = 3
