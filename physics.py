"""
Module qui gère la physique dans le jeux
Ce module est composé d'une liste d'appel qui est calqué sur la fonction de translation
La translation via des vecteurs vitesses
"""
from typing import Callable

from CONSTS import coordinate, MILITICK, NB_PX_LEFT_RIGHT, SENS_DIRECT, SENS_INDIRECT
from entity import Entity
from utils import get_full_line

all_moves: list[list[float | float | list[list[bool]] | Entity | bool | int | Callable]] = list()
map: object = None

def def_map(map_local: object) -> None:
    global map
    map = map_local

def addtomove(v_init: float, alpha: float, entity: Entity, callback: Callable):
    entity.synchroniseXY()
    all_moves.append([v_init, alpha, entity, True, 0, callback])


def translation(v_init: float, alpha: float, entity: Entity, force: bool, local_tick: int
                ) -> tuple[bool, bool, None | float]:
    """
    Calcul la position d'une Entity au prochain tick
    :param v_init: Vistesse initiale
    :param alpha: angle en radian (sens direct)
    :param map: map sous le format de Map.map
    :param entity: Entity qui va être modifié
    :param force: Décrit si on est dans la phase initiale de décolage du saut
    :param local_tick: Tick initiale (tick au moment du départ i.e. ce n'est pas zéro)
    :return: tuple (Arrêt du mouvment, sommes nous dans un mode de force ?, vitesse à l'impact si impact sinon None)
    """
    # prox = reduce(lambda pre, nex: pre or nex,
    #               [map[entity.x + X][entity.y + Y] for X in range(-1, 2) for Y in range(-1, 2)]
    #               )
    # if force or not prox:
    for militick in range(0, MILITICK):
        temp = entity.x, entity.y
        entity.move_to(local_tick, v_init, alpha, 1 / MILITICK)

        # if not map[entity.x][entity.y + 1]:
        #    force = False
        # print(entity.x)
        if map[entity.x, entity.y]:
            force = False

            lst = get_full_line(temp, (entity.x, entity.y))
            if lst[0] == temp:
                # Extérieur à 0
                step = 1
                i = 0
            else:
                # Exterieur à la fin
                step = -1
                i = len(lst) - 1

            impact = lst[i]
            while (not map[lst[i][0], lst[i][1]]) and 0 <= i < len(lst):
                impact = lst[i]
                i += step

            entity.x, entity.y = impact

            x, y = entity.get_speed(local_tick, v_init, alpha)
            return True, force, (x ** 2 + y ** 2) ** 0.5
    return False, force, None


def get_right_left_px(px: coordinate, _from: coordinate) -> tuple[coordinate, coordinate]:
    """
    Cacul les pixels droits et gauches du pixel d'impact
    :param px: pixel d'impact dans le sol
    :param _from: pixel d'impact de surface
    :return: Pixel Droit, Pixel Gauche
    """
    visited = set(px)
    from_right = _from
    from_left = _from
    freeze_right = False
    freeze_left = False

    # Recherche du début du sens direct pour vérifier _from pixel.
    ptr = 0
    x, y = px[0] - _from[0], px[1] - _from[1]
    while ((x, y) != SENS_DIRECT[ptr] and ptr < 8):
        ptr += 1
    if (ptr == 8):
        raise AssertionError("px pixel and _from pixel are not contiguously")

    for i in range(NB_PX_LEFT_RIGHT):

        # Right first
        ptr = 0
        x, y = px[0] - from_right[0], px[1] - from_right[1]
        while ((x, y) != SENS_DIRECT[ptr]):
            ptr += 1
        if not freeze_right:
            for j in range(1, len(SENS_DIRECT)):
                x, y = SENS_DIRECT[(ptr + j) % len(SENS_DIRECT)]
                if map[from_right + x, from_right + y] and (x, y) not in visited:
                    visited.add((x, y))
                    from_right = x, y
                    break
            else:
                freeze_right = True

        # Left then
        ptr = 0
        x, y = px[0] - from_left[0], px[1] - from_left[1]
        while ((x, y) != SENS_INDIRECT[ptr]):
            ptr += 1
        last = from_left
        if not freeze_left:
            for j in range(1, len(SENS_INDIRECT)):
                x, y = SENS_INDIRECT[(ptr + j) % len(SENS_INDIRECT)]
                if map[from_left + x, from_left + y] and (x, y) not in visited:
                    last = (x, y)

            if last == from_left:
                freeze_left = True
            else:
                visited.add(last)
                from_left = last


    return from_right, from_left
