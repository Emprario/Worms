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
from numpy import array

from CONSTS import coordinate, OnLoadMapError, DEFAULT_DENSITY, SIMULTANITY_THRESHOLD, MIN_SIMULTANITY_THRESHOLD
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
    """
    "Peint" une surface fmap de la "couleur" `not base` à partir des points `centers` en se délimitant aux contours :
    `segmap` dans le respect des dimensions implicites.
    :param segmap: Une liste des contours à respecter
    :param fmap: Le calque de la map
    :param centers: Les points qui seront propagateurs
    :param dim: Les dimensions
    :param base: La couleur de fond de la map
    """

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
        self.texture: array = None  # Invalid texture is None - debug // list[int] is bytes to print img
        self.fond: array = None
        # self.pxd_array: array = None
        self.dimensions: list[int] = [0, 0]
        self.destruction_stack: list[tuple[coordinate, float]] = []
        self.ONMAPs: dict[int, list[list[bool]]] = {i: [] for i in range(SIMULTANITY_THRESHOLD)}
        self.available_ONMAPs: [int] = []
        self.clear_ONMAPs: [int] = [i for i in range(SIMULTANITY_THRESHOLD)]
        self.reset_ONMAP_thread: Thread | None = None
        self.px_update_list: set[tuple[int, int]] = set()
        self.Surf: pygame.Surface | None = None

        # Lock vars
        self.askforlocking: bool = False
        self.active_update_texture: int = 0

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
                                    self.fond = pygame.image.load(sp[1]).convert_alpha()
                                elif sp[0] == "full":
                                    print("load front")
                                    # pygame.image.tobytes returns [y] then [x]
                                    self.texture = pygame.image.load(sp[1]).convert_alpha()

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

        self.Surf = pygame.Surface(self.dimensions)
        # self.texture = pygame.surfarray.map_array(self.Surf, self.texture)
        # self.fond = pygame.surfarray.map_array(self.Surf, self.fond)
        # self.pxd_array = self.texture.copy()

        print("Array Copied !")
        ###   #####   ###

        # Step2: Obtain segmented map

        form_borders: list[list[coordinate]] = gen_segmented_map(vectmap)

        # Step 3: Fill the map !
        self.clear_map()

        """
        Cette méthode de remplissage est optimisé ne sachant pas forcement le centre des formes.
        La génération de la map s'effectue au début du programme pour rendre les fichiers de maps bien plus légés et 
        pour permettre dans de futures mis-à-jours de générer des maps aléatoires plus facilements.
        """
        for form in form_borders:

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

        self.__start_filter_image((0, 0), self.dimensions)

    def clear_map(self):
        """
        Method to clear the actual map
        """
        self.map = [
            [False for _ in range(self.dimensions[1])] for _ in range(self.dimensions[0])
        ]

    def update_texture(self, *, all_pxs: bool = False):
        """
        Affiche la map dans le screen
        Utilise les textures internes
        :param all_pxs: Paramètre à placer en keyword, il force une actualisation de TOUS les pixels
        """
        if all_pxs:
            self.__start_filter_image((0, 0), self.dimensions)

        pixels = pygame.surfarray.pixels_alpha(self.texture)
        try:
            while len(self.px_update_list) > 0:
                self.update_px(pixels, self.px_update_list.pop())
        except KeyError:
            pass
        del pixels

        if self.texture.get_locked():
            return
        try:
            self.Surf.blit(self.fond, (0, 0))
            self.Surf.blit(self.texture, (0, 0))
        except pygame.error:
            while self.texture.get_locked():
                continue
            self.Surf.blit(self.fond, (0, 0))
            self.Surf.blit(self.texture, (0, 0))

    def update_px(self, pixels, coo: coordinate):
        """
        Blit the pixel given on screen
        :param pixels: Alpha channel of main texture
        :param coo: Coord du pixel
        """
        x, y = coo
        if not (0 <= x < self.dimensions[0] and 0 <= y < self.dimensions[1]):
            raise ValueError(x, y)
        if self.map[x][y]:
            pixels[x, y] = 255
        else:
            pixels[x, y] = 0

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

        while len(self.available_ONMAPs) == 0:
            continue
        AX = self.available_ONMAPs.pop()

        algo_peinture(seg_circle, self.ONMAPs[AX], [impact], self.dimensions, base=True)

        for x in range(xmini, xmaxi + 1):
            for y in range(ymini, ymaxi + 1):
                self.map[x][y] = self.map[x][y] and self.ONMAPs[AX][x][y]

        head = (xmini, ymini)
        queue = (xmaxi, ymaxi)

        self.clear_ONMAPs.append(AX)
        if not self.reset_ONMAP_thread.is_alive():
            self.reset_ONMAP_thread = Thread(group=None, target=self.__reset_ONMAP, name=None)
            self.reset_ONMAP_thread.start()

        self.__start_filter_image(head, queue)

        Thread(group=None, target=self.update_texture, name=None).start()

    # @add_time_incache
    def __start_filter_image(self, head, queue):
        """
        Envoie dans la liste d'update tous les pixels dans le rectangle head à queue
        :param head: Premier point (en haut à gauche)
        :param queue: Dernier point (en bas à droite)
        """
        for x in range(head[0], queue[0]):
            for y in range(head[1], queue[1]):
                self.px_update_list.add((x, y))

    def __reset_ONMAP(self):
        """
        Reset les caches de l'écriture de la map 1 à 1
        """
        while len(self.clear_ONMAPs) > 0:
            AX = self.clear_ONMAPs.pop()
            # self.ONMAPs[AX] = deepcopy(self.TRUEMAP)
            self.ONMAPs[AX] = [[True for _ in range(self.dimensions[1])] for _ in range(self.dimensions[0])]
            self.available_ONMAPs.append(AX)


if __name__ == "__main__":
    map = TileMap("assets/map/01.map")
    map.print_map(map.map)
