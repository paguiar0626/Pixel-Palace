import pygame

import audio
from menus import MainMenu
from player import Player
from screen import Screen
from ui_builder import UiBuilder
from read_txtfile import WrapText

class Game:

    _player: Player = Player()
    _screen: Screen

    def __init__(self, screen_width: int, screen_height: int, surface: pygame.surface.Surface):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._surface = surface

    @property
    def screen(self) -> Screen:
        return self._screen

    @screen.setter
    def screen(self, screen: Screen):
        self._screen = screen

    @property
    def surface(self) -> pygame.surface.Surface:
        return self._surface

    @property
    def player(self) -> Player:
        return self._player

    def start(self):
        self._screen = MainMenu(self)
        clock = pygame.time.Clock()
        ui = UiBuilder(self._surface, self._screen_height, self._screen_width)
        text_wrapper = WrapText(self._surface, self._screen_height, self._screen_width)

        while True:
            clock.tick(30)
            # CAUTION: calling pygame.event.get() multiple times per frame *will* prevent some inputs from registering
            # Instead, get the event list once and pass it to methods as needed
            event_list = pygame.event.get()

            self._screen.tick(event_list)
            self._screen.handle_input()
            self._screen.draw(ui, text_wrapper)

            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()
            audio.play_background_music()
