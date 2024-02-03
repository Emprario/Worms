"""
Gestion de la physique pure
    - Equations physique en jeu
    - PAS DE CONSTANTES (cf. CONSTS.py)
"""
from math import pi, cos, sin, atan

import pygame

from CONSTS import coordinate, vector


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

    return list(zip([round(center[0] + int(radius * cos(angle)), 4) for angle in angles],
                    [round(center[1] + int(radius * sin(angle)), 4) for angle in angles]))


def get_result_point_from_vector(vector0: vector) -> coordinate:
    """
    Get the point at the end of the vector
    :param vector0: Vecteur à extraire la position
    :return: Point (arrondi)
    """
    return vector0[0][0] + int(vector0[1] * cos(vector0[2])), vector0[0][1] + int(vector0[1] * sin(vector0[2]))


def get_dist(ptA: coordinate, ptB: coordinate) -> float:
    """
    Calcule la distance entre 2 points
    :param ptA: Point A
    :param ptB: Point B
    :return: Distance
    """
    return ((ptA[0] - ptB[0]) ** 2 + (ptA[1] - ptB[1]) ** 2) ** 0.5


def get_angle(ptA: coordinate, ptB: coordinate) -> float:
    """
    Calcul l'angle entre 2 points
    :param ptA: Point A (Origine de l'angle)
    :param ptB: Point B
    :return: Angle (rad)
    """
    # On place p1 à gauche de p2
    if ptA[0] > ptB[0]: ptA, ptB = ptB, ptA
    if ptA[0] - ptB[0] == 0:
        if ptA[1] > ptB[1]:
            return pi / 2
        else:
            return -pi / 2
    return atan(ptA[1] - ptB[1]) / (ptA[0] - ptB[0])


def get_full_line(ptA: coordinate, ptB: coordinate) -> list[coordinate]:
    """
    Get a full line with all coordinates between ptA and ptB
    :param ptA: Point A
    :param ptB: Point B
    :return: List of all points between
    """
    # Use the bresenham algorithm
    # Reference : https://fr.wikipedia.org/wiki/Algorithme_de_trac%C3%A9_de_segment_de_Bresenham
    # Reference : https://www.geeksforgeeks.org/bresenhams-line-generation-algorithm/

    # Fit the input into the algorithm:
    if ptA[0] > ptB[0]:
        ptA, ptB = ptB, ptA
    print(ptA, ptB)

    dx = ptB[0] - ptA[0]
    dy = ptB[1] - ptA[1]
    if dx < dy:
        invert_x_y = True
        ptA = (ptA[1], ptA[0])
        ptB = (ptB[1], ptB[0])
    else:
        invert_x_y = False

    # Bresenham algorithm
    line = []
    m = 2 * (ptB[1] - ptA[1])
    correction = m - (ptB[0] - ptA[0])

    y = ptA[1]
    for x in range(ptA[0], ptB[0] + 1):
        line.append((x, y))
        correction += m

        if correction >= 0:
            y += 1
            correction -= 2 * (ptB[0] - ptA[0])

    if invert_x_y:
        for i in range(len(line)):
            line[i] = (line[i][1], line[i][0])
    return line


def does_intersect(point: coordinate, line: tuple[coordinate, coordinate]) -> bool:
    """
    Défini si un point et une ligne s'intersectent
    :param point: Point
    :param line: Ligne
    :return: True Si Point \in Ligne
    """
    pass


def is_inner_point(point: coordinate, polygon: list[coordinate]) -> bool:
    """
    Défini si un point est dans un polygone
    :param point: Point à définir
    :param polygon: Tous les points des polygones
    :return: Si le point est dans le polygone
    """
    inside = False
    # On prend les points deux à deux
    for i in range(len(polygon)):
        p1, p2 = polygon[i - 1], polygon[i]

        # On place p1 à gauche de p2
        if p1[0] > p2[0]: p2, p1 = p1, p2
        # print("P1={}, P2={} ...".format(p1, p2))

        # Test si le point pourrait être dans le champ de la droite deux points (niveau y)
        if min(p1[1], p2[1]) <= point[1] <= max(p1[1], p2[1]):
            # print("In y range")
            if p2[0] <= point[0]:
                # print("Out in x range (no intersection)")
                continue
            elif point[0] <= p1[0]:
                # print("Out in x range (intersect segment)")
                inside = not inside
            else:
                # print("In x range")
                for pt in range(point[0], p2[0]):
                    rect = pygame.Rect(pt, point[1], 1, 1)
                    if rect.clipline((p1, p2)) != ():
                        # print(f"Inverting {inside}->{not inside}")
                        inside = not inside
                        break
        else:
            # print("Out y range")
            continue
    # print(f"Res={inside}")
    return inside


if __name__ == '__main__':
    pts = [(3, 2), (15, 5)]
    print(get_full_line(*pts))
    pts = [(5, 15), (2, 3)]  # Inversion
    print(get_full_line(*pts))
