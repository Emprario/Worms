"""Outil de création de map pour développeur"""

import pygame

##############################
#       CONSTS Wrapper       #
##############################

SIZE: tuple[int, int] = (1080, 720)
MAP_KEYWORD: str = "STARTSTOP"


##############################
#          mainloop          #
##############################

def mainloop():
    while True:

        # Blit
        display.blit(FOND, (0, 0))
        for pointer in registered_points_list:
            if len(pointer) >= 1:
                display.blit(pointer[0][0], reel_pos(pointer[0][1]))
            for i in range(1, len(pointer)):
                display.blit(pointer[i][0], reel_pos(pointer[i][1]))
                pygame.draw.line(display, (255, 255, 255), pointer[i - 1][1], pointer[i][1])
            if len(pointer) >= 2:
                pygame.draw.line(display, (255, 255, 255), pointer[0][1], pointer[-1][1])
        # if len(points) >= 1:
        #    display.blit(points[0][0], reel_pos(points[0][1]))
        # for i in range(1, len(points)):
        #    display.blit(points[i][0], reel_pos(points[i][1]))
        #    pygame.draw.line(display, (255, 255, 255), points[i - 1][1], points[i][1])
        pygame.display.flip()

        # Events
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    with open(MAP_FILE, "w") as map:
                        for pointer in registered_points_list:
                            map.write(MAP_KEYWORD + '\n')
                            for point in pointer:
                                map.write(str(point[1][0]) + ' ' + str(point[1][1]) + '\n')

                    pygame.quit()
                    exit(0)
                case pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Clique Gauche
                        posx, posy = pygame.mouse.get_pos()
                        print("Position : ", posx, posy)
                        add_new_point(posx, posy)
                    elif event.button == 3:  # Clique Droit
                        if len(points) > 2:  # Don't act if there's no at least 3 points
                            # Don't register point
                            points.append((pygame.image.load("./target_15x15.png"), points[0][1]))
                            registered_points_list.append([])
                            points.clear()


def add_new_point(posx: int, posy: int):
    point = (pygame.image.load("./target_15x15.png"), (posx, posy))
    points.append(point)
    registered_points_list[-1].append(point)


def reel_pos(pos: tuple[int, int]) -> tuple[int, int]:
    return pos[0] - 7, pos[1] - 7


if __name__ == "__main__":
    pygame.init()
    # Display
    display = pygame.display.set_mode(SIZE)
    # Titre
    pygame.display.set_caption("DevTool for map creation")
    # Active Scene settings
    FOND = pygame.Surface(SIZE)
    FOND.fill((173, 216, 230))

    MAP_FILE = "./dummy.map"

    points: list[tuple[pygame.surface, tuple[int, int]]] = []
    registered_points_list: list[list[tuple[pygame.surface, tuple[int, int]]]] = [[]]

    # AVERTISSEMENT
    for _ in range(10):
        print("IL FAUT REMPLIR LES MAPS DANS LE SENS HORAIRE OBLIGATOIREMENT !!!!!!!!!!!")
    mainloop()
