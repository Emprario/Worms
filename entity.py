"""
Class qui gère les entity
"""
from map import Map


class Entity:
    map_obj = None

    def __init__(self, map: Map = None):
        if map is not None:
            self.map_obj = map

    def meth1(self):
        pass

    def move_worm_check(self):
        """

        """



