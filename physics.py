"""
Module qui gère la physique dans le jeux
Ce module est composé d'une liste d'appel qui est calqué sur la fonction de translation
La translation via des vecteurs vitesses
"""
from typing import Callable
from math import atan, pi

from CONSTS import coordinate, MILITICK, NB_PX_LEFT_RIGHT, SENS_DIRECT, SENS_INDIRECT, REMOTE_POINT, MIN_SPEED_BOUNCE, BOUNCING
from entity import Entity
from utils import get_full_line
from map import TileMap

all_moves: list[list[float | float | Entity | bool | int | list[coordinate] | Callable]] = list()
map: TileMap | None = None


def def_map(map_local: TileMap) -> None:
    global map
    map = map_local


def addtomove(v_init: float, alpha: float, entity: Entity, callback: Callable):
    entity.synchroniseXY()
    all_moves.append([v_init, alpha, entity, True, 0, [(entity.x, entity.y)], callback])


def translation(v_init: float, alpha: float, entity: Entity, force: bool, local_tick: int, trace: list[coordinate]
                ) -> tuple[bool, bool, float | None, coordinate | None]:
    """
    Calcul la position d'une Entity au prochain tick
    :param v_init: Vistesse initiale
    :param alpha: angle en radian (sens direct)
    :param entity: Entity qui va être modifié
    :param force: Décrit si on est dans la phase initiale de décolage du saut
    :param local_tick: Tick initiale (tick au moment du départ i.e. ce n'est pas zéro)
    :return: tuple (Arrêt du mouvment, sommes nous dans un mode de force ?, vitesse à l'impact si impact sinon None)
    """
    # prox = reduce(lambda pre, nex: pre or nex,
    #               [map[entity.x + X][entity.y + Y] for X in range(-1, 2) for Y in range(-1, 2)]
    #               )
    # if force or not prox:
    if map[entity.x, entity.y]:
        raise AssertionError("Worm already in the wall")

    for militick in range(0, MILITICK):
        temp = (entity.x, entity.y)
        entity.move_to(local_tick, v_init, alpha, 1 / MILITICK)

        if map[entity.x, entity.y]:
            force = False

            lst = get_full_line(temp, (entity.x, entity.y))

            if map[temp] or not map[entity.x, entity.y]:
                print(entity)
                print(map[entity.x, entity.y])
                print(map[temp])
                raise AssertionError("Inner point and outter point are outter before")

            if lst[0] == temp:
                # <=> premier élément à m'extérieur de la map
                step = 1
                i = 0
            else:
                # <=> dernier élément à m'extérieur de la map
                step = -1
                i = len(lst) - 1

            impact = lst[i]
            i += step
            next_point = lst[i]
            while (not map[next_point]) and 0 <= i < len(lst):
                print("mv upper")
                impact = lst[i]
                i += step
                next_point = lst[i]

            if not map[next_point] or map[impact]:
                raise AssertionError("Inner point and outter point are outter after")

            entity.x, entity.y = impact
            trace.append((entity.x, entity.y))
            x, y = entity.get_speed(local_tick, v_init, alpha)
            return True, force, (x ** 2 + y ** 2) ** 0.5, next_point
    trace.append((entity.x, entity.y))
    return False, force, None, None


def move_entities():
    """
    Make a single movement of all entities
    """
    i = 0
    while i < len(all_moves):
        # print(tick, [move[3] for move in all_moves])
        result = translation(*all_moves[i][:-1])
        # print(result)
        all_moves[i][-4] = result[1]
        all_moves[i][-3] += 1
        if result[0] and result[2] < MIN_SPEED_BOUNCE:
            print("I: Killed")
            all_moves[i][-1](*all_moves[i][:-1], result[2])
            #print(all_moves[i][2])
            del all_moves[i]
        elif result[0] and result[2] > MIN_SPEED_BOUNCE:
            entity = all_moves[i][2]
            next_point = result[-1]
            callback = all_moves[i][-1]
            v_impact = result[2]
            trace = all_moves[i][-2].copy()
            del all_moves[i]
            bounce(entity, next_point, callback, v_impact, trace)
        else:
            i += 1


def get_right_left_px(px: coordinate, _from: coordinate) -> tuple[coordinate, coordinate]:
    """
    Calcule les pixels droits et gauches du pixel d'impact
    :param px: pixel d'impact dans le sol
    :param _from: pixel d'impact de surface
    :return: Pixel Droit, Pixel Gauche
    """
    visited = {_from, px}
    from_right = _from
    from_left = _from
    actual_right = px
    actual_left = px
    freeze_right = False
    freeze_left = False

    # Recherche du début du sens direct pour vérifier _from pixel.
    x, y = px[0] - _from[0], px[1] - _from[1]
    if (x, y) not in SENS_DIRECT:
        raise AssertionError("px pixel and _from pixel are not contiguously")

    for i in range(NB_PX_LEFT_RIGHT):

        # Right first
        ptr = 0
        x, y = actual_right[0] - from_right[0], actual_right[1] - from_right[1]
        while (x, y) != SENS_DIRECT[ptr]:
            ptr += 1
        if not freeze_right:
            for j in range(1, len(SENS_DIRECT)):
                x, y = SENS_DIRECT[(ptr + j) % len(SENS_DIRECT)]
                if map[actual_right[0] + x, actual_right[1] + y] and (x, y) not in visited:
                    ac = (actual_right[0] + x, actual_right[1] + y)
                    visited.add(ac)
                    from_right = actual_right
                    actual_right = ac
                    break
            else:
                freeze_right = True

        # Left then
        ptr = 0
        x, y = actual_left[0] - from_left[0], actual_left[1] - from_left[1]
        while ((x, y) != SENS_INDIRECT[ptr]):
            ptr += 1
        if not freeze_left:
            for j in range(1, len(SENS_INDIRECT)):
                x, y = SENS_INDIRECT[(ptr + j) % len(SENS_INDIRECT)]
                if map[actual_left[0] + x, actual_left[1] + y] and (x, y) not in visited:
                    ac = (actual_left[0] + x, actual_left[1] + y)
                    visited.add(ac)
                    from_left = actual_left
                    actual_left = ac
                    break
                else:
                    freeze_left = True

    return actual_right, actual_left


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


def get_remote_point_from_curve(full_line: list[coordinate]) -> coordinate:
    """
    Calcul du point antérieur de la courbe pour un calcul de l'angle d'impact.
    :param full_line: Liste des derniers points dans l'ordre anti-chronologique
    :return: remote point
    """
    if len(full_line) < REMOTE_POINT:
        return full_line[0]
    else:
        return full_line[-REMOTE_POINT]


# v_init: float, alpha: float, entity: Entity, force: bool, local_tick: int, trace: list[coordinate]
# list[float | float | Entity | bool | int | list[coordinate] | Callable | coordinate]
def bounce(entity: Entity, next_point: coordinate, callback : Callable, v_impact, trace) -> None:
    """
    Rebond un point et ajout avec addtomove
    :param args: Arguments conventionnel de la gravité
    """
    entity = entity
    impact_pt = entity.x, entity.y
    print(entity, impact_pt)
    ground_pt = next_point
    r_pix, l_pix = get_right_left_px(impact_pt, ground_pt)
    better_x, better_y = impact_pt[0] - (r_pix[0] - l_pix[0]), impact_pt[1] - (r_pix[1] - l_pix[1])  # creating parallel to r_pix l_pix
    butter_l_pix: coordinate = (better_x, better_y)
    surf_angle = get_angle(impact_pt, butter_l_pix)
    trajectory_angle = get_angle(get_remote_point_from_curve(trace), butter_l_pix)
    impact_angle = trajectory_angle + surf_angle
    addtomove(BOUNCING*v_impact, -impact_angle, entity, callback) #

