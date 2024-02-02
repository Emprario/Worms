"""
Gestion de la physique pure
    - Equations physique en jeu
    - PAS DE CONSTANTES (cf CONSTS.py)
"""
from math import pi, cos, sin

import pygame

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


def is_inner_point(point: coordinate, polygon: list[coordinate]) -> bool:
    """
    Défini si un point est dans un polygone
    :param point: Point à définir
    :param polygon: Tous les points du polygones
    :return: Si le point est dans le polygone
    """
    inside = False
    # On prend les points deux à deux
    for i in range(len(polygon)):
        p1, p2 = polygon[i - 1], polygon[i]

        # On place p1 à gauche de p2
        if p1[0] > p2[0]: p2, p1 = p1, p2
        print("P1={}, P2={} ...".format(p1, p2))

        # Test si le point pourrait être dans le champ de la droite deux points (niveau y)
        if min(p1[1], p2[1]) <= point[1] <= max(p1[1], p2[1]):
            print("In y range")
            if p2[0] <= point[0]:
                print("Out in x range (no intersection)")
                continue
            elif point[0] <= p1[0]:
                print("Out in x range (intersect segment)")
                inside = not inside
            else:
                print("In x range")
                for pt in range(point[0], p2[0]):
                    rect = pygame.Rect(pt, point[1], 1, 1)
                    if rect.clipline((p1, p2)) != ():
                        print(f"Inverting {inside}->{not inside}")
                        inside = not inside
                        break
        else:
            print("Out y range")
            continue
    print(f"Res={inside}")
    return inside
