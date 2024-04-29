"""
Map management
Méthode de gestion de map : tilemap
    - Comment la charger depuis un fichier externe (assets/map/??.map)
    - Comment représenter dans le programme de la matière
"""

from functools import reduce
from sys import setrecursionlimit
from threading import Thread

import pygame

from CONSTS import coordinate, OnLoadMapError, DEFAULT_DENSITY, SIMULTANITY_THRESHOLD, MIN_SIMULTANITY_THRESHOLD
from debug_pygame import get_point_from_idx
from utils import get_full_line, get_circle

# from time import time

setrecursionlimit(9000000)


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


def algo_peinture(segmap: list[list[coordinate]], fmap: list[list[bool]], centers: list[coordinate],
                  dim: list[int], base: bool = False):
    def fill_neighbours(point: coordinate, segform: set[coordinate]):
        # print(segform)
        fmap[point[0]][point[1]] = not base
        for (x, y) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (
                    0 <= point[0] + x < dim[0] and 0 < point[1] + y <= dim[1] and
                    (point not in segform) and fmap[point[0] + x][point[1] + y] == base
            ):
                fill_neighbours((point[0] + x, point[1] + y), segform)

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
        self.map: list[list[bool]] = []  # [x][y]
        self.texture: list[int] | None = None  # Invalid texture is None - debug // list[int] is bytes to print img
        self.fond: list[int] | None = None
        self.dimensions: list[int] = [0, 0]
        self.form_borders: list[list[coordinate]] = []
        self.destruction_stack: list[tuple[coordinate, float]] = []
        self.ONMAPs: dict[int, list[list[bool]]] = {i: [] for i in range(SIMULTANITY_THRESHOLD)}
        self.available_ONMAPs: [int] = []
        self.clear_ONMAPs: [int] = [i for i in range(SIMULTANITY_THRESHOLD)]
        self.reset_ONMAP_thread: Thread | None = None
        self.px_update_list: set[int] = set()

        # Step 1: Extract vectorial map

        """
        Load map from file.
        On notera que la fonction n'hésitera pas à renvoyer des OnLoadMapError pour tout désagraments
        La fonction modifie également les dimensions de la map qui est donné
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
                            if newrecord and self.dimensions != [0, 0]:
                                vectmap.append([])
                                newrecord = False
                            elif self.dimensions == [0, 0]:
                                raise OnLoadMapError("Les dimensions n'ont pas été initialisées")

                            try:
                                sp = line.split(' ')
                                if len(sp) != 2:
                                    raise ValueError
                                x, y = int(sp[0]), int(sp[1])  # Erreur de conversion → ValueError
                                if x < 0 or x > self.dimensions[0] or y < 0 or y > self.dimensions[1]:
                                    raise ValueError

                            except ValueError:
                                raise OnLoadMapError(
                                    f"Le module python ne peut pas extraire deux coordonées valides pour : {line}\n" \
                                    "Regardez éventuellement de les dimensions"
                                )
                            else:
                                vectmap[-1].append((x, y))

                        case "DIMENSIONS":
                            if self.dimensions != [0, 0]:
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
                                self.dimensions[0] = x
                                self.dimensions[1] = y

                        case "TEXTUREPATH":
                            if texture is not None:
                                raise OnLoadMapError("La texture a déjà été initialisée")

                            sp = line.split(' ')
                            print(sp)

                            try:
                                print((sp[0] != "empty") ^ (sp[0] != "full"))
                                if len(sp) != 2 or not ((sp[0] != "empty") ^ (sp[0] != "full")):
                                    raise IndexError
                                if line != "notprovided":
                                    open(sp[1], 'r')
                            except IndexError:
                                raise OnLoadMapError("Écriture incorrect dans les textures : <full|empty> chemin")
                            except FileNotFoundError:
                                raise OnLoadMapError("Impossible de trouver le fichier de texture")
                            else:
                                if sp[0] == "empty":
                                    print("load fond")
                                    self.fond = list(pygame.image.tobytes(pygame.image.load(sp[1]), 'ARGB'))
                                elif sp[0] == "full":
                                    print("load front")
                                    # pygame.image.tobytes returns [y] then [x]
                                    self.texture = list(pygame.image.tobytes(pygame.image.load(sp[1]), 'ARGB'))

        # print("VectMap chargé avec :")
        # print(self.dimensions)
        # print(self.texture)
        # print(len(vectmap))
        # print(vectmap)

        ### INTERLUDE ###
        self.reset_ONMAP_thread = Thread(group=None, target=self.__reset_ONMAP, name=None)
        self.reset_ONMAP_thread.start()
        while len(self.available_ONMAPs) < MIN_SIMULTANITY_THRESHOLD:
            continue

        self.Surf = pygame.Surface((self.dimensions[0], self.dimensions[1]))
        ###   #####   ###

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
        # print (have_duplicated_obj_in_list(segmap))

        # Step 3: Fill the map !
        self.clear_map()

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
                # print(point)
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
            ORDER_START = [(0, True), (0, False), (-1, True), (-1, False), (1, True), (1, False)]
            ORDER_END = [(0, False), (0, True), (1, False), (1, True), (-1, False), (-1, True)]

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
                                        # if (x,y) in {(100,200),(200, 200)}: print("IN",x, chkset[y, x-idx])
                                        if (y, x - idx) in chkset and chkset[y, x - idx] == state:
                                            checkedas = True  # C'est une extremite
                                        elif (y, x - idx) in chkset and chkset[y, x - idx] == (
                                                not state):  # Dans le même état
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
                                # print(Hdict[y])
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
                if not insidetable[y + 1] and not insidetable[y - 1] and insidetable[y]:
                    # print(f"There's a bug in y = {y}")
                    inside = False
                    for x in range(max_W + 1, min_W - 1, -1):
                        if x in Hdict[y] and x - 1 not in Hdict[y]:  # On est en bout
                            inside = not inside
                        elif x not in Hdict[y]:
                            self.map[x][y] = inside

        self.__filter_image(0, len(self.texture), arbitrary=True)

    def __getitem__(self, item: coordinate) -> bool:
        if (
                type(item) != tuple or len(item) != 2 or type(item[0]) != int or type(item[1]) != int
                or item[0] < 0 or item[0] >= self.dimensions[0] or item[1] < 0 or item[1] >= self.dimensions[1]
        ):
            raise ValueError
        return self.map[item[0]][item[1]]

    def __setitem__(self, item: coordinate, value: bool):
        if (
                type(item) != tuple or len(item) != 2 or type(item[0]) != int or type(item[1]) != int
                or type(value) != bool
                or item[0] < 0 or item[0] >= self.dimensions[0] or item[1] < 0 or item[1] >= self.dimensions[1]
        ):
            raise ValueError
        self.map[item[0]][item[1]] = value


    def get_dimensions(self):
        return self.dimensions.copy()

    def clear_map(self):
        """
        Method to clear the actual map
        """
        self.map = [
            [False for _ in range(self.dimensions[1])] for _ in range(self.dimensions[0])
        ]

    def print_map(self):
        """
        Affiche la map dans un écran à part
        Utilité pour le débugage
        :param skelmap: La map à afficher
        """
        self.Surf.lock()
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if self.map[x][y]:
                    self.Surf.set_at((x, y), pygame.Color("red"))
                else:
                    self.Surf.set_at((x, y), pygame.Color("black"))
        self.Surf.unlock()

    def blit_texture(self, *, all_pxs: bool = False):
        """
        Affiche la map dans le screen
        Utilise les textures internes
        :param screen: Le screen qu'on doit blit dessus
        """
        if all_pxs:
            self.Surf.blit(pygame.image.frombytes(bytes(self.fond), self.dimensions, 'ARGB'), (0, 0))
            self.Surf.blit(pygame.image.frombytes(bytes(self.texture), self.dimensions, 'ARGB'), (0, 0))
        else:
            # self.Surf.lock()
            pxarray = pygame.surfarray.pixels2d(self.Surf)
            while len(self.px_update_list) > 0:
                self.update_px(pxarray, self.px_update_list.pop())
            del pxarray
            # self.Surf.unlock()

    def update_px(self, pxarray, idx: int) -> None:
        """
        Blit the pixel given on screen
        :param idx: Pixel index in self.texture (should point on Alpha channel)
        :param screen: The screen to update
        """
        x, y = get_point_from_idx(idx)
        if self.texture[idx] == 255:
            # self.Surf.set_at((x, y), self.texture[idx + 1:idx + 4])
            r, g, b = self.texture[idx + 1:idx + 4]
        elif self.texture[idx] == 0:
            # self.Surf.set_at((x, y), self.fond[idx + 1:idx + 4])
            r, g, b = self.fond[idx + 1:idx + 4]
        else:
            raise AttributeError("An alpha channel should be either 0 or 255")
        pxarray[x, y] = (r * 256 * 256) + (g * 256) + b

    def void_destruction_stack(self):
        """
        Loop to empty the destruction stack
        """
        while len(self.destruction_stack) > 0:
            Thread(group=None, target=self.destroy_map, name=None, args=self.destruction_stack.pop()).start()

    # @get_time
    def destroy_map(self, impact: coordinate, power: float):
        """
        Destoy the map using an impact point and the power of the weapon
        i.e. it's modifying the self.map var
        :param impact: coordoniate of the point of the center of the impact
        :param power: the power of the weapon which is the radius of the impact
        """
        circle = get_circle(DEFAULT_DENSITY, impact, power)

        xmini = reduce(lambda tpA, tpB: tpA if tpA[0] < tpB[0] else tpB, circle)[0]
        xmaxi = reduce(lambda tpA, tpB: tpA if tpA[0] > tpB[0] else tpB, circle)[0]
        ymini = reduce(lambda tpA, tpB: tpA if tpA[1] < tpB[1] else tpB, circle)[1]
        ymaxi = reduce(lambda tpA, tpB: tpA if tpA[1] > tpB[1] else tpB, circle)[1]

        seg_circle = gen_segmented_map([circle])

        # for point in seg_circle[0]:
        #     show_point(point, does_stop=False, one_pixel=True)
        # show_point(impact, color=(0,0,255))

        while len(self.available_ONMAPs) == 0:
            # print("Available :", self.available_ONMAPs)
            # print("To clean :", self.clear_ONMAPs)
            continue
        AX = self.available_ONMAPs.pop()

        algo_peinture(seg_circle, self.ONMAPs[AX], [impact], self.dimensions, base=True)

        # t1 = time()
        for x in range(xmini, xmaxi + 1):
            for y in range(ymini, ymaxi + 1):
                self.map[x][y] = self.map[x][y] and self.ONMAPs[AX][x][y]
        # t2 = time()
        # print(t2 - t1)

        head = (xmini, ymini)
        # queue = (xmaxi, ymaxi)
        starter = (head[0] + head[1] * self.dimensions[0]) * 4
        # goal = (queue[0] + queue[1] * self.dimensions[0]) * 4
        # show_point(head, does_stop=False)
        # show_point(queue)

        self.clear_ONMAPs.append(AX)
        if not self.reset_ONMAP_thread.is_alive():
            self.reset_ONMAP_thread = Thread(group=None, target=self.__reset_ONMAP, name=None)
            self.reset_ONMAP_thread.start()

        # self.tt = 0
        parter = (xmaxi - xmini) * 4
        # print(parter, goal, starter)
        launch_dicts = [{'_from': starter + self.dimensions[0] * i * 4,
                         '_to': starter + parter + self.dimensions[0] * (i + 1) * 4}
                        for i in range(ymaxi - ymini)]
        Thread(group=None, target=self.__start_filter_image, name=None, args=launch_dicts).start()
        # for dlign in launch_dicts:
        #     self.__filter_image(**dlign)

    # @add_time_incache
    def __start_filter_image(self, *launch_dict: dict[str, int]) -> None:
        for dict in launch_dict:
            self.__filter_image(**dict)

    def __filter_image(self, _from: int, _to: int, *, arbitrary: bool = False) -> None:
        """
        Filter the image to set alpha channel of hidden pixel to 0 and the other pixel to 1
        :param _from: Start processing at px _from (included)
        :param _to: Ends processing at px _to (excluded)
        """
        # print("go from", _from, "to", _to)
        # t1 = time()
        # Make sure we are interacting with images
        assert self.texture != None
        if arbitrary:
            for idx in range(_from, _to, 4):  # Catch only alpha channels
                # print((idx // 4) // self.dimensions[0], (idx // 4) // self.dimensions[1])
                if self.map[(idx // 4) % self.dimensions[0]][(idx // 4) // self.dimensions[0]]:
                    self.texture[idx] = 255
                else:
                    self.texture[idx] = 0
        else:
            for idx in range(_from, _to, 4):  # Catch only alpha channels
                x, y = (idx // 4) % self.dimensions[0], (idx // 4) // self.dimensions[0]
                if (
                        self.map[x][y]
                        and self.texture[idx] != 255
                ):
                    self.texture[idx] = 255
                    self.px_update_list.add(idx)
                elif (
                        not self.map[x][y]
                        and self.texture[idx] != 0
                ):
                    self.texture[idx] = 0
                    self.px_update_list.add(idx)

        # t2 = time()
        # self.tt += t2 - t1

    def __reset_ONMAP(self):
        while len(self.clear_ONMAPs) > 0:
            AX = self.clear_ONMAPs.pop()
            # self.ONMAPs[AX] = deepcopy(self.TRUEMAP)
            self.ONMAPs[AX] = [[True for _ in range(self.dimensions[1])] for _ in range(self.dimensions[0])]
            self.available_ONMAPs.append(AX)


if __name__ == "__main__":
    map = TileMap("assets/map/01.map")
    map.print_map(map.map)
