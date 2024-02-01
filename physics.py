"""
Gestion de la physique pure
    - Equations physique en jeu
    - PAS DE CONSTANTES (cf CONSTS.py)
"""
from math import pi, cos, sin
from CONSTS import coordinate


class BimBamBoum:
    """Moteur physique du jeu"""
    pass


def get_circle(density: int, center: coordinate, radius: float) -> list[coordinate]:
    """
    Renvoie une liste de coordonée en forme de cercle,
    en renvoie selon la densité demandée
    :param density: Nombre de points renvoyé
    :param center: Centre du cercle (coordonnée)
    :param radius: Rayon du cercle
    :return: Liste de coordonnée
    """
    angles = [(2 * k * pi) / density for k in range(density)]

    return zip([round(center[0] + radius * cos(angle), 4) for angle in angles],
               [round(center[1] + radius * sin(angle), 4) for angle in angles])
