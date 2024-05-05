"""
Module qui gère la physique dans le jeux
Ce module est composé d'une liste d'appel qui est calqué sur la fonction de translation
La translation via des vecteurs vitesses
"""
from entity import Entity
from CONSTS import coordinate, MILITICK
from utils import get_full_line
from typing import Callable
from functools import reduce


all_moves: list[list[float, float, list[list[bool]], Entity, bool, int, Callable]] = list()

# var: Callable = translation
"""
fall: Callable = fall_damage

def fall_damage(velocity: float, cst: int):     
    if velocity > cst:
        return (velocity-cst) * x  # x to define -> depend on player max HP
"""

def addtomove(append: list[float, float,list[list[bool]], Entity, bool, int, Callable]):
    append[3].synchroniseXY()
    all_moves.append(append)

def translation(v_init: float, alpha: float, map: list[list[bool]], entity: Entity, force: bool, local_tick: int
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
        if map[entity.x][entity.y]:
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
            while (not map[lst[i][0]][lst[i][1]]) and 0 <= i < len(lst):
                impact = lst[i]
                i += step

            entity.x, entity.y = impact

            x, y = entity.get_speed(local_tick, v_init, alpha)
            return True, force, (x ** 2 + y ** 2) ** 0.5
        return False, force, None
    x, y = entity.get_speed(local_tick, v_init, alpha)
    return True, force, (x ** 2 + y ** 2) ** 0.5