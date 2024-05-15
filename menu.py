from typing import Callable
from pygame import Surface
import pygame

from CONSTS import GAME_NAME


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


class Text:
    def __init__(self, x: int, y: int, text: str, font: pygame.font.Font, shadow=False):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.shadow = shadow

    def draw(self, screen: Surface):
        if self.shadow:
            shadow_surface = self.font.render(self.text, False, (0, 0, 0))
            screen.blit(shadow_surface, (self.x+5, self.y+5))
        text_surface = self.font.render(self.text, False, (255, 255, 255))
        screen.blit(text_surface, (self.x, self.y))


class Menu:
    def __init__(self, title: str, width: int, height: int, background: Surface, buttons: list[Button] = [],
                 texts: list[Text] = []):
        self.title = title
        self.width = width
        self.height = height
        self.background = pygame.transform.scale(background, (width, height))
        self.buttons: list[Button] = buttons
        self.texts: list[Text] = texts

    def draw(self, screen: Surface):
        pygame.display.set_caption(GAME_NAME + " - " + self.title)
        screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw(screen)
        for text in self.texts:
            text.draw(screen)

    def on_click(self, mouse: tuple[int, int]):
        for button in self.buttons:
            button.on_click(mouse)
