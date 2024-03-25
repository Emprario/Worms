"""
Map management
Méthode de gestion de map : tilemap
    - Comment la charger depuis un fichier externe (assets/map/??.map)
    - Comment représenter dans le programme de la matière
"""

from CONSTS import coordinate, OnLoadMapError, DEFAULT_DENSITY
from utils import get_full_line, get_circle
#from debug_pygame import show_point
from sys import setrecursionlimit


setrecursionlimit(90000000)


def load_from_file(mappath: str, dimensions: list[int]) -> tuple[str, list[list[coordinate]]]:
    """
    Load map from file.
    On notera que la fonction n'hésitera pas à renvoyer des OnLoadMapError pour tout désagraments
    La fonction modifie également les dimensions de la map qui est donné
    :param mappath: Chemin vers la map
    :param dimensions: Dimension qui vont être modifié
    :return: la texture et le fichier vectoriel de map
    """
    texture: str | None = None
    vectmap: list[list[coordinate]] = []
    record: str = ""
    newrecord: bool = False
    with open(mappath, "r") as file:
        for line in file:

            # Remove last carriage return
            if line[-1] != '\n':
                raise OnLoadMapError(f"All lines should end with \\n\nline=\"{line}\"")
            line = line[:-1]

            if line == "STARTSTOP" or line == "DIMENSIONS" or line == "TEXTUREPATH":
                record = line
                newrecord = True

                # Check si vectmap n'est pas vide et dans ce cas s'il a au moins 3 points dedans
                if len(vectmap) > 0 and len(vectmap[-1]) < 2:
                    raise OnLoadMapError("Une forme ne possède pas au moins 3 points")

            else:
                match record:
                    case "STARTSTOP":
                        if newrecord and dimensions != [0, 0]:
                            vectmap.append([])
                            newrecord = False
                        elif dimensions == [0, 0]:
                            raise OnLoadMapError("Les dimensions n'ont pas été initialisées")

                        try:
                            sp = line.split(' ')
                            if len(sp) != 2:
                                raise ValueError
                            x, y = int(sp[0]), int(sp[1])  # Erreur de conversion → ValueError
                            if x < 0 or x > dimensions[0] or y < 0 or y > dimensions[1]:
                                raise ValueError

                        except ValueError:
                            raise OnLoadMapError(
                                f"Le module python ne peut pas extraire deux coordonées valides pour : {line}\n" \
                                "Regardez éventuellement de les dimensions"
                            )
                        else:
                            vectmap[-1].append((x, y))

                    case "DIMENSIONS":
                        if dimensions != [0, 0]:
                            raise OnLoadMapError("Les dimensions ont déjà été initialisées")

                        try:
                            sp = line.split(' ')
                            if len(sp) != 2:
                                raise ValueError
                            x, y = int(sp[0]), int(sp[1])  # Erreur de conversion → ValueError
                            if x <= 0 or y <= 0:
                                raise ValueError

                        except ValueError:
                            raise OnLoadMapError(
                                f"Le module python ne peut pas extraire deux longueurs valides pour : {line}"
                            )
                        else:
                            dimensions[0] = x
                            dimensions[1] = y

                    case "TEXTUREPATH":
                        if texture is not None:
                            raise OnLoadMapError("La texture a déjà été initialisée")

                        try:
                            if line != "notprovided":
                                open(line, 'r')
                        except FileNotFoundError:
                            raise OnLoadMapError("Impossible de trouver le fichier de texture")
                        else:
                            texture = line

    return texture, vectmap


def gen_segmented_map(vectmap: list[list[coordinate]]) -> list[list[coordinate]]:
    """
    Génère une map avec les points donnés relié entre-eux deux à deux
    :param vectmap: Map vectoriel composé de points isolé
    :return: Map segmenté avec des lignes continues avec des formes non pleines
    """
    segmap: list[list[coordinate]] = []
    for form in vectmap:
        segmap.append([])
        for i in range(len(form)):
            line = get_full_line(form[i - 1], form[i], True)
            segmap[-1].extend(line)
            del segmap[-1][len(segmap[-1]) - len(line)]  # Il est toujours généré en double
    return segmap


def algo_peinture(segmap: list[list[coordinate]], fmap: list[list[bool]], centers: list[coordinate], base: bool = False):

    def fill_neighbours(point: coordinate, segform: set[coordinate]):
        # print(segform)
        fmap[point[0]][point[1]] = not base
        for (x,y) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (point not in segform) and fmap[point[0]+x][point[1]+y] == base:
                fill_neighbours((point[0]+x, point[1]+y), segform)

    # print(centers)
    for i in range(len(centers)):
        fill_neighbours(centers[i], set(segmap[i])) 


class TileMap:
    """Représentation de la map en mémoire via une TileMap"""

    def __init__(self, mappath: str):
        """
        Constructeur de la classe
        :param mappath: Chemin (relatif depuis la root du projet) vers la map
        """
        self.map: list[list[bool]] = []
        self.texture: str | None = None  # Invalid texture is None // "notprovided" is for debug texture
        self.dimensions: list[int] = [0, 0]
        self.form_borders: list[list[coordinate]] = []

        # Step 1: Extract vectorial map

        self.texture, vectmap = load_from_file(mappath, self.dimensions)

        # print("VectMap chargé avec :")
        # print(self.dimensions)
        # print(self.texture)
        # print(len(vectmap))
        # print(vectmap)

        # Step2: Obtain segmented map

        self.form_borders: list[list[coordinate]] = gen_segmented_map(vectmap)

        # more = {point for lstpoint in segmap for point in lstpoint}
        # skelmap = [[(x,y) in more for y in range(self.dimensions[1])] for x in range(self.dimensions[0])]
        # self.print_map(skelmap)


        # print("Map à segments généré avec :")
        # print(len(segmap) == len(vectmap))
        # print(segmap)
        # print(segmap[0])
        # [show_point(point, does_stop=False) for form in segmap for point in form]
        # print(have_duplicated_obj_in_list(segmap))

        # Step 3: Fill the map !

        self.map = [
            [False for _ in range(self.dimensions[1])] for _ in range(self.dimensions[0])
        ]

        for form in self.form_borders:

            # Step 3.1 Order points by x then y in a dict
            # it's a set because 'in' operator in set is O(1) in python same for dicts

            # Hdict contains every X points in a Y lign
            Hdict: dict[int, set[int]] = dict()
            # Wpresence is every point that exists in every Y lign
            Wpresence: set[int] = set()
            max_W = form[0][0]
            min_W = form[0][0]

            for point in form:
                #print(point)
                if point[0] < min_W:
                    min_W = point[0]
                elif point[0] > max_W:
                    max_W = point[0]
                Wpresence.add(point[0])
                if point[1] not in Hdict:
                    Hdict[point[1]] = {point[0]}
                else:
                    Hdict[point[1]].add(point[0])

            # Step 3.2 Fill the line

            insidetable = [False] * self.dimensions[1]

            # Set for pending checks // x ← True if the record is upper False if the record is Down
            chkset: dict[coordinate, bool] = {}

            # x ← True si c'est une extrémité False sinon | None si non statuée
            checkedas: bool | None = None

            # Orders - Start then End
            ORDER_START = [(0, True), (0, False), (-1, True),  (-1, False), (1, True), (1, False)]
            ORDER_END = [(0, False), (0, True), (1, False),  (1, True), (-1, False), (-1, True)]

            for x in range(1, self.dimensions[0] - 1):
                if x in Wpresence:
                    for y in range(1, self.dimensions[1] - 1):
                        # Rien ne sert de Tester si y n'est pas dans le Hdict
                        if y in Hdict and x in Hdict[y]:

                            ### ANALYSE D'EXTREMITÉ ###
                            checkedas = None

                            # Si y existe et alors check si x n'est pas au centre d'une ligne
                            if (does_end := x + 1 not in Hdict[y]) or x - 1 not in Hdict[y]:
                                # Find first point of the line:
                                idx = 0
                                while x - idx - 1 in Hdict[y]:
                                    idx += 1
                                # if (x, y) in {(100,200),(200, 200)}:
                                #     print(x - idx, Hdict[y - 1] if y - 1 in Hdict else None, Hdict[y + 1] if y + 1 in Hdict else None)
                                for cp in (ORDER_END if does_end else ORDER_START):
                                    i = cp[0]
                                    state = cp[1]
                                    side = -1 if state else 1
                                    # Order (i, side): (-1, -1), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 1)
                                    # Analyse s'il y a une connection en haut et en bas avec un point qui existe
                                    # par défaut cette partie n'engendre rien sinon
                                    if y + side in Hdict and x + i in Hdict[y + side] and checkedas is None:
                                        #if (x,y) in {(100,200),(200, 200)}: print("IN",x, chkset[y, x-idx])
                                        if (y, x - idx) in chkset and chkset[y, x - idx] == state:
                                            checkedas = True  # C'est une extremite
                                        elif (y, x - idx) in chkset and chkset[y, x - idx] == (not state):  # Dans le même état
                                            checkedas = False
                                        else:
                                            chkset[y, x - idx] = state

                                # match (x, y):
                                #     case (100, 200):
                                #         print("== DEBUG 100,200 ==")
                                #         print(chkset[200,100])
                                #         print(checkedas)
                                #     case (200, 200):
                                #         print("== DEBUG 200,200 ==")
                                #         print(chkset[200,100])
                                #         print(checkedas)


                            ### SWITCHS DU INSIDE ###
                            # Check si on a affaire à un point qui en bout de chaine
                            if x + 1 not in Hdict[y]:
                                #print(Hdict[y])
                                if checkedas is None:
                                    raise AssertionError(
                                        "Checkedas n'est pas censé ne pas être défini <=> Le point n'est pas connecté !"
                                    )
                                if not checkedas:  # Ce n'est pas une extrémité
                                    insidetable[y] = not insidetable[y]

                            ### RÉPLICATION DE LA MAP ###

                        # Add x to the trace
                        if y in Hdict and x in Hdict[y]:
                           self.map[x][y] = True


                        # Add x to fullfilled the inside status of y
                        if y in Hdict and insidetable[y]:
                            self.map[x][y] = True

            # Clean Up !
            for y in range(1, self.dimensions[1] - 1):
                # ... 0 0
                # ... X X
                # ... 0 0
                if not insidetable[y+1] and not insidetable[y-1] and insidetable[y]:
                    # print(f"There's a bug in y = {y}")
                    inside = False
                    for x in range(max_W + 1, min_W-1, -1):
                        if x in Hdict[y] and x - 1 not in Hdict[y]:  # On est en bout;
                            inside = not inside
                        elif x not in Hdict[y]:
                            self.map[x][y] = inside


    def print_map(self, skelmap: list[list[bool]], screen):
        """
        Affiche la map dans un écran à part
        Utilité pour le débugage
        :param skelmap: La map à afficher
        """
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if skelmap[x][y]:
                    screen.set_at((x, y), "red")
                else:
                    screen.set_at((x, y), "black")


    def destroy_map(self, impact: coordinate, power:float):
        """
        Destoy the map using an impact point and the power of the weapon
        i.e. it's modifying the self.map var
        :param impact: coordoniate of the point of the center of the impact
        :param power: the power of the weapon which is the radius of the impact
        """
        
        seg_circle = gen_segmented_map([get_circle(DEFAULT_DENSITY, impact, power)])
        
        # for point in seg_circle[0]:
        #     show_point(point, does_stop=False, one_pixel=True)
        # show_point(impact, color=(0,0,255))

        onmap = [[True for y in range(len(self.map[x]))] for x in range(len(self.map))]

        algo_peinture(seg_circle, onmap, [impact], base=True)

        self.map = [[self.map[x][y] and onmap[x][y] for y in range(len(self.map[x]))] for x in range(len(self.map))]


    def update_contour(self):
        """
        
        """
        # self.form_borders
        pass


if __name__ == "__main__":
    map = TileMap("assets/map/01.map")
    map.print_map(map.map)
