from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

from button import Button
from player import Player
from ui_builder import UiBuilder

# Prevents circular import
if TYPE_CHECKING:
    from game import Game


class Screen(ABC):
    _game: "Game"
    _player: Player
    _buttons: list[Button]

    def __init__(self, game: "Game"):
        self._game = game
        self._player = game.player
        self._buttons = []

    @abstractmethod
    def tick(self, event_list: list[pygame.event.Event]):
        ...

    @abstractmethod
    def handle_input(self):
        ...

    @abstractmethod
    def draw(self, ui: UiBuilder):
        ...
