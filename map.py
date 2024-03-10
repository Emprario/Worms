"""
Map management
La méthode de gestion des maps reste à déterminer
    - Comment la charger depuis un fichier externe (assets/map/??.map)
    - Comment représenter dans le programme de la matière
"""

from random import randint

from CONSTS import MAP_KEYWORD_REGISTRATION, MAP_KEYWORD_TEXTURE, DEFAULT_DENSITY, coordinate
from debug import *
from physics import get_circle, is_inner_point, does_intersect
from weapons import Weapon


class Map:
    """Représentation de la Map sous forme d'un objet"""

    def __init__(self, mappath: str):
        """Chargement de la map dans un objet (chargement logique)."""
        self.map: list[list[
            coordinate]] = []  # coordinate : tuple (int,int); then list(coordinate) liste of tuples for a polygon; then list of all of em
        self.texture: str = ''
        register_texture = False
        with open(mappath, "r") as file:
            for line in file:
                if register_texture:
                    self.texture = line[:-1]
                elif line == MAP_KEYWORD_REGISTRATION + '\n':
                    self.map.append([])
                elif line == MAP_KEYWORD_TEXTURE + '\n':
                    register_texture = True
                elif line == '\n':
                    continue
                else:
                    try:
                        spline = line.split()
                        if int(spline[0]) < 0 or int(spline[1]) < 0:
                            raise ValueError
                        self.map[-1].append((int(spline[0]), int(spline[1])))
                    except (ValueError, IndexError):
                        if len(line) > 0 and line[-1] == '\n':
                            line = line[:-1]
                        else:
                            line = line
                        raise ValueError(
                            f"Le valeur de '{line}' ne peut être convertie en coordonnée, est-il bien composer de deux"
                            f" entiers positif ?"
                        )
        for i in range(len(self.map)):
            if len(self.map[i]) < 3:
                raise ValueError(f'Map {i + 1} incomplète est composé que de {len(self.map[i])} éléments')

    def destroy_map(self, impact: coordinate, weapon: Weapon):
        """
        Enregistre une destruction de la map, utilise un point d'impact et une arme caractéristique ansi qu'une puissance
        :param impact: Position (x, y)
        :param weapon: Arme utilisée
        """
        # Step 1 : Draw a circle
        circle = get_circle(DEFAULT_DENSITY, impact, weapon.power)

        # Step 2 : Get sequences of inner point
        # two tuple of two breakpoints <- seq of points
        inners: dict[tuple[tuple[coordinate, coordinate], tuple[coordinate, coordinate]], list[coordinate]] = {}
        continuation = False
        buffkey: tuple[coordinate, coordinate] = None
        buffer: list[coordinate] = []
        for form in self.map:
            for ptidx in range(len(circle)):
                if is_inner_point(circle[ptidx], form):
                    # Catch if we are already registering ...
                    if continuation:
                        buffer.append(circle[ptidx])
                    # Check if it's not the first point
                    elif ptidx > 0 and not continuation:
                        continuation = True
                        for formptidx in range(len(form)):
                            if does_intersect(
                                    (circle[ptidx - 1], circle[ptidx]),
                                    (form[formptidx - 1], form[formptidx])
                            ):
                                buffkey = (form[formptidx - 1], form[formptidx])
                                break
                        inners[buffkey] = [circle[ptidx]]
                    elif not continuation:
                        pass

        """        
                if is_inner_point(point, form):
                    if i in inners and continuation:
                        inners[i][-1].append(point)
                    elif i in inners and not continuation:
                        inners[i].append([point])
                    else:  # i not in inners
                        inners[i] = [[point]]
                    continuation = True
                    placed.append(i)

                    break
            else:
                placed.append(-1)
                continuation = False

        # Update last list to eventually connect to it
        if placed[0] != -1 and placed[-1] != -1:
            copy: list[coordinate] = []
            for nend in range(len(inners[placed[-1]])):
                if circle[0] in inners[placed[0]][nend]:
                    copy = inners[placed[0]][nend]
                    del inners[placed[0]][nend]
                    break
            for nstart in range(len(inners[placed[-1]])):
                if circle[-1] in inners[placed[-1]][nstart]:
                    inners[placed[0]][nstart].extend(copy)
                    break
        """

        # Two sequences of points in a same key means it should be divided into two diff polygones

        # Step 3 : contact points association + add point to self.map
        registered_predecessors: list[coordinate] = []
        # Parcours à la fois les listes à insérer et lindex du polygone dans self.map
        for idx, all_seqs in inners.items():
            pointer: int = 0
            id_seq = 0

            # Cherche tant qu'on n'a pas fait toutes les séquences
            while id_seq < len(all_seqs) and pointer < len(self.map[idx]):

                # Check si un point d'origine est blown
                if (
                        is_inner_point(self.map[idx][pointer], circle) and
                        # self.map[idx][pointer - 1] not in registered_predecessors and
                        not is_inner_point(self.map[idx][pointer - 1], circle)
                ):
                    # en def un prédécesseur
                    del self.map[idx][pointer]
                    registered_predecessors.append(self.map[idx][pointer])

                    # on enregistre les points et ajuste les suites
                    for idx_insertion in range(len(all_seqs[id_seq])):
                        self.map[idx].insert(pointer, all_seqs[id_seq][idx_insertion])
                    pointer += len(all_seqs[id_seq])
                    id_seq += 1
                elif is_inner_point(self.map[idx][pointer], circle):
                    del self.map[idx][pointer]
                else:
                    pointer += 1
            if id_seq < len(all_seqs) and pointer == len(self.map[idx]):
                raise AssertionError("Shouldn't be here !!")

        # Check seq of points
        sq = dict()
        dmrun = True
        while dmrun:
            for all_seq_point in inners.values():
                for seq_point in all_seq_point:
                    if tuple(seq_point) not in sq:
                        sq[tuple(seq_point)] = (randint(0, 255), randint(0, 255), randint(0, 255))
                    for point in seq_point:
                        pygame.draw.circle(DEBUG_SCREEN, sq[tuple(seq_point)], point, 5)
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    dmrun = False

        # Step 4 : Delete every over point inside the circle Except newly incerted ones
        """i = 0
        while i < len(self.map):
            j = 0
            form = self.map[i]
            # print(form)
            while j < len(form):
                # print((form[j][0], form[j][1]), " <-in?->", is_inner_point((form[j][0], form[j][1]), circle),
                #      "&& not part of circle ?", (form[j][0], form[j][1]) not in circle)
                if (form[j][0], form[j][1]) not in circle and is_inner_point((form[j][0], form[j][1]), circle):
                    # print("Deleting :", i, j)
                    del self.map[i][j]
                else:
                    j += 1
            # On ne peut pas dessiner de polygone à moins de 3 côtés
            if len(form) < 3:
                del self.map[i]
            else:
                i += 1"""

    def print_map(self, surface: pygame.Surface, *, highlight_points: bool = False):
        """
        Chargerment de la map avec des couleurs vives, les points peuvent être affichés ! (Débogage)
        :param surface: surface sur lequel afficher
        :param highlight_points: Permet d'afficher les points
        """
        for points in self.map:
            pygame.draw.polygon(surface, "darkblue", points)
        if highlight_points:
            for points in self.map:
                for point in points:
                    pygame.draw.circle(surface, (0, 255, 0), point, 5)

    def pg_blit(self, surface: pygame.Surface):
        """Pygame Blit : Fonction d'affichage spécifique à la map"""
        # Crée l'image
        ld_texture = pygame.image.load(self.texture).convert_alpha()

        # Crée la surface de polygones
        mask_surface = pygame.Surface(surface.get_size())
        for points in self.map:
            pygame.draw.polygon(mask_surface, "white", points)

        # Imprime EN multipliant la couleur des pixels (i.e. en restant assez fidèle) :
        # Reference : https://github.com/pygame/pygame/blob/main/src_c/surface.h#L247
        ld_texture.blit(mask_surface, (0, 0), None, pygame.BLEND_RGBA_MULT)
        # Cette texture modifiée est blit
        surface.blit(ld_texture, (0, 0))


if __name__ == "__main__":
    mapobj = Map("./assets/map/dummy.map")

    run = True
    while run:
        # print(pygame.mouse.get_pos())
        clear_screen()
        # mapobj.print_map(DEBUG_SCREEN, True)
        mapobj.pg_blit(DEBUG_SCREEN)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                mapobj.destroy_map((490, 157), Weapon(None))
