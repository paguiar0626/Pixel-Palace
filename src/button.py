from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Iterable

import pygame

import audio
from ui_builder import UiBuilder

# Prevents circular import
if TYPE_CHECKING:
    from card import Card
    from game import Game
    from player import Player
    from screen import Screen


class Button(ABC):
    """A UI element that performs some action when clicked."""
    _game: "Game"
    _rect: pygame.rect.Rect
    _on_clicked: Callable

    @abstractmethod
    def draw(self, surface: pygame.surface.Surface):
        ...

    def check_for_click(self, mouse_events: Iterable[pygame.event.Event]):
        for click in mouse_events:
            if self._rect.collidepoint(click.pos):
                self._on_clicked()
                audio.play(audio.Sounds.generic_button)


class ImageButton(Button):
    """A button attached to a static image."""

    def __init__(self, game: "Game", rect: pygame.rect.Rect, texture_path: str, on_clicked: Callable):
        self._game = game
        self._rect = rect
        self._on_clicked = on_clicked

        self._texture = pygame.image.load(texture_path)

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(pygame.transform.scale(
            self._texture, self._rect.size), self._rect.topleft)


class TextButton(Button):
    """A button attached to text."""

    def __init__(self, game: "Game", coords: tuple[int, int], text: str, font_size: int, on_clicked: Callable):
        self._game = game
        self._text = text
        self._font_size = font_size
        self._on_clicked = on_clicked

        self._rect = pygame.rect.Rect(coords, (0, 0))

    def draw(self, surface: pygame.surface.Surface):
        font = pygame.font.Font(UiBuilder.font_filepath, self._font_size)
        text = font.render(self._text, True, "white")
        self._rect = pygame.rect.Rect(
            self._rect.x, self._rect.y, text.get_width(), text.get_height())
        surface.blit(text, self._rect.topleft)


def callback(func: Callable):
    """Makes a function return a reference to itself instead of executing when called."""
    def wrapper(*args, **kwargs) -> Callable:
        def inner():
            func(*args, **kwargs)
        return inner
    return wrapper


def for_all_methods(decorator: Callable):
    """Apply a decorator to all methods of a class."""
    # https://stackoverflow.com/a/6307868
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


@for_all_methods(callback)
# Applying staticmethod with the above decorator causes a whole host of typing errors
class ButtonCallbacks:
    """Defines available behaviors for buttons when clicked."""
    @staticmethod
    def placeholder():
        pass

    @staticmethod
    def load_screen(screen: type["Screen"], game: "Game", *args):
        game.screen = screen(game, *args)

    @staticmethod
    def return_to_screen(screen: "Screen", game: "Game"):
        game.screen = screen

    @staticmethod
    def update_bet(player: "Player", delta: int):
        def clamp(n, min_, max_):
            """Ensure that a value falls between a specified min and max range."""
            return max(min(max_, n), min_)

        player.bet = clamp(player.bet + delta, 0, player.balance)

    @staticmethod
    def flip_card_face_up(card: "Card"):
        if not card.is_face_up:
            card.flip()

    @staticmethod
    def reset_balance(player: "Player"):
        player.reset_balance()

    @staticmethod
    def update_music_volume(delta: float):
        from audio import change_music_volume
        change_music_volume(delta)

    @staticmethod
    def update_sfx_volume(delta: float):
        from audio import change_sfx_volume
        change_sfx_volume(delta)

    @staticmethod
    def set_CF_bet_heads(player: "Player"):
        player.choice = "heads"

    @staticmethod
    def set_CF_bet_tails(player: "Player"):
        player.choice = "tails"
