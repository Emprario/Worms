from typing import Callable
from pygame import Surface
import pygame

import CONSTS


class Button:
    def __init__(self, x: int, y: int, image: Surface, scale: float, action: Callable):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action

    def draw(self, screen: Surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def on_click(self, mouse: tuple[int, int]):
        if self.rect.collidepoint(mouse):
            self.action()


class Menu:
    def __init__(self, title: str, width: int, height: int, background: Surface, buttons: list[Button]):
        self.title = title
        self.width = width
        self.height = height
        self.background = pygame.transform.scale(background, (width, height))
        self.buttons: list[Button] = buttons

    def draw(self, screen: Surface):
        #pygame.draw.rect(screen, (24, 0, 0, 1), (0, 0, self.width, self.height))
        screen.blit(self.background, (0, 0))
        print("Drawing menu : " + self.title)
        for button in self.buttons:
            button.draw(screen)

    def on_click(self, mouse: tuple[int, int]):
        for button in self.buttons:
            button.on_click(mouse)
