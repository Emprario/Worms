"""
Module de définitions de constantes élémentaires à travers tout le programme.
Il faut veiller à n'importer aucun module dans celui-ci sauf des modules externes.
Merci de mettre des hints sur les constantes dans le programme afin de faciliter leurs utilisations.
"""

from math import pi


# Constantes
GAME_NAME = "PalaVect2"
WINDOW_SIZE = (1920, 1080)
SPAWN_POINTS = [(415, 120), (1779, 397), (1190, 142), (1390, 642), (758, 714), (343, 717)]
COLORS = ['red', 'green', 'blue', 'gold', 'gray', 'cyan', 'orange', 'purple', 'black', 'violet', 'yellow', 'white']
PLAYERS = 3
DEBUG = False

DEFAULT_DENSITY = 20  # Densité pour le traçage de cercle
MAX_THREAD_BY_CALC = 1  # Depreceated
SIMULTANITY_THRESHOLD = 64  # Nombre maximum de cache qui est généré
MIN_SIMULTANITY_THRESHOLD = 32  # Nombre minimum de cache pour démarer le programme
G = 0.075  # G : la constante de gravité
FRAMERATE = 60  # Le framerate à atteindre (capé)
MILITICK = 50  # Subdivision du tick pour décomposer le mouvement.
NB_PX_LEFT_RIGHT = 1  # Nb de pixel parcourue à droite et à gauche du pixel d'impact, donne une précision
# Sur la normale de l'impact
SENS_DIRECT = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
# Défini le sens direct (selon l'orientation pygame de l'axe y)
SENS_INDIRECT = SENS_DIRECT[::-1]  # Défini le sens indirect (selon l'orientation pygame de l'axe y)
REMOTE_POINT = 10  # Défini le nombre de point qu'il remonter à l'arrière
MIN_SPEED_BOUNCE = 1  # Défini la speed minimum pour rebondir
BOUNCING = 0.3
FALL_LIMIT = 20
AUTO_MOUNT = 4
COEF_DIST_DAMAGE = 80
MIN_SPEED_DAMAGE = 3.5
JUMP = 3


coordinate = tuple[int, int]  # Alias pour les coordonées


# Errors
class OnLoadMapError(Exception):
    pass
