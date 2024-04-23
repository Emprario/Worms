"""
Utilitaire commun pour diverses opérations
"""

from math import cos, sin, pi

from CONSTS import coordinate


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


def get_full_line(ptA: coordinate, ptB: coordinate, strict_order: bool = False) -> list[coordinate]:
    """
    Get a full line with all coordinates between ptA and ptB
    :param ptA: Point A
    :param ptB: Point B
    :return: List of all points between
    """
    # Use the bresenham algorithm
    # Reference : https://fr.wikipedia.org/wiki/Algorithme_de_trac%C3%A9_de_segment_de_Bresenham
    # Reference : https://babavoss.pythonanywhere.com/python/bresenham-line-drawing-algorithm-implemented-in-py

    # Fit the input into the algorithm:
    if (invert_points := ptA[0] > ptB[0]):
        ptA, ptB = ptB, ptA
    # print(ptA, ptB)

    dx = ptB[0] - ptA[0]
    dy = abs(ptB[1] - ptA[1])
    if dx < dy:
        dy, dx = dx, dy
        invert_x_y = True
        ptA = (ptA[1], ptA[0])
        ptB = (ptB[1], ptB[0])
    else:
        invert_x_y = False

    # Bresenham algorithm

    x, y = ptA
    pente = 2 * dy - dx
    line = [(x, y)]

    for k in range(2, dx + 2):
        if pente > 0:
            y = y + 1 if y < ptB[1] else y - 1
            pente = pente + 2 * (dy - dx)
        else:
            pente = pente + 2 * dy
        x = x + 1 if x < ptB[0] else x - 1
        line.append((x, y))

    # Correct inversion
    if invert_x_y:
        for i in range(len(line)):
            line[i] = (line[i][1], line[i][0])

    if strict_order and invert_points:
        anti = []
        for coo in line:
            anti.insert(0, coo)
        return anti

    return line