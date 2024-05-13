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

    def onClick(self, mouse: tuple[int, int]):
        if self.rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0] == 1:
                self.action()


class Menu:
    def __init__(self, title: str, width: int, height: int, background: Surface, buttons: list[Button]):
        self.title = title
        self.width = width
        self.height = height
        self.background = background
        self.buttons = buttons

    def draw(self, screen: Surface):
        print("Drawing menu : " + self.title)
        for button in self.buttons:
            button.draw(screen)

    def onClick(self, mouse: tuple[int, int]):
        for button in self.buttons:
            button.onClick(mouse)

