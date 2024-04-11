from entity import Entity
from CONSTS import coordinate
from utils import get_full_line
from typing import Callable

all_moves: list[tuple[float, float, list[list[bool]], coordinate, Entity, bool, int, Callable]] = list()

# var: Callable = translation
"""
fall: Callable = fall_damage

def fall_damage(velocity: float, cst: int):
    if velocity > cst:
        return (velocity-cst) * x  # x to define -> depend on player max HP
"""


def translation(v_init: float, alpha: float, map: list[list[bool]], point0: coordinate, entity: Entity,
                force: bool, local_tick: int) -> tuple[bool, bool, None | float]:
    """"""
    if force or (not map[entity.x][entity.y + 1] and not map[entity.x][entity.y]):
        temp = entity.x, entity.y
        entity.move_to(local_tick, v_init, alpha, *point0)
        x, y = entity.get_speed(local_tick, v_init, alpha)
        # print(x, y)
        v_impact = (x ** 2 + y ** 2) ** 0.5

        if not map[entity.x][entity.y + 1]:
            force = False
        # print(entity.x)
        if map[entity.x][entity.y]:
            entity.x, entity.y = temp  # passera forcément par else avant de passer par if sinon assertionError

            while not map[entity.x][entity.y]:
                temp = (entity.x, entity.y)
                entity.move_to(local_tick, v_init, alpha, *point0)  # angle a modifier pour généraliser
                # entity.get_speed(tick0 - tick, 0.1, 0)
                local_tick += 0.05

            temp = (temp[0], temp[1])
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

        return False, force, v_impact
    return True, force, None
