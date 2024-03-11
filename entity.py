"""
Class qui gère les entity
"""
from map import Map
from physics import get_angle, get_dist, get_full_line

class Entity:
    map_obj = None

    def __init__(self, map: Map = None):
        if map is not None:
            self.map_obj = map

    def meth1(self):
        pass
    def print_coords(self):
        """

        """
        for i in range(0, len(self.map_obj.map)):

            print(("Coordinates of polygon number {}", format(i)))

            for j in range(0, len(self.map_obj.map[i])-1):

                print("Coordinate x, y :", self.map_obj.map[i][j])
                new_line = get_full_line(self.map_obj.map[i][j], self.map_obj.map[i][j+1])
                print(new_line)

    def check_y_coord(self, y_position):
        """

        """





mappp = Map("assets/map/dummy.map")

testing = Entity(mappp)
testing.print_coords()
