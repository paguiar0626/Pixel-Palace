from typing import TYPE_CHECKING

import pygame

import audio
from button import ButtonCallbacks, ImageButton, TextButton
from minigames.coin_flip import CoinFlip
from minigames.memory import MemorySetup
from minigames.blackjack import BlackJack
from hud_builder import HUDBuilder
from screen import Screen
from ui_builder import UiBuilder
from hud_builder import HUDBuilder
from read_txtfile import ReadInstructions, WrapText

# Prevents circular import
if TYPE_CHECKING:
    from game import Game


class MainMenu(Screen):
    def __init__(self, game: "Game"):
        super().__init__(game)
        instructions = ReadInstructions("info_texts/menu_info.txt")

        self._buttons.extend([
            TextButton(game, (550, 250), "Coin Flip", 40,
                       ButtonCallbacks.load_screen(CoinFlip, game)),
            TextButton(game, (550, 350), "Blackjack",
                       40, ButtonCallbacks.load_screen(BlackJack, game)),
            TextButton(game, (550, 450), "Memory", 40,
                       ButtonCallbacks.load_screen(MemorySetup, game)),
            TextButton(game, (100, game.surface.get_height() - 75), "Credits",
                       40, ButtonCallbacks.load_screen(Credits, game)),
        ])

        self._buttons.extend(HUDBuilder.get_hud_buttons(game, "menu"))

    def tick(self, event_list: list[pygame.event.Event]):
        for button in self._buttons:
            button.check_for_click(
                filter(lambda event: event.type == pygame.MOUSEBUTTONUP, event_list))

    def handle_input(self):
        ...

    def draw(self, ui: UiBuilder, text_wrapper: WrapText):
        ui.set_background(pygame.image.load('assets/background.jpg'))
        ui.draw_top_bar(self._player)
        ui.draw_title("Welcome to Pixel Palace!", (255, 255, 255))

        for button in self._buttons:
            button.draw(self._game.surface)

class Credits(Screen):
    def __init__(self, game: "Game"):
        super().__init__(game)

        self._buttons.extend(HUDBuilder.get_hud_buttons(game, "menu"))

    def tick(self, event_list: list[pygame.event.Event]):
        for button in self._buttons:
            button.check_for_click(
                filter(lambda event: event.type == pygame.MOUSEBUTTONUP, event_list))

    def handle_input(self):
        ...

    def draw(self, ui: UiBuilder, text_wrapper: WrapText):
        ui.set_background(
            pygame.image.load('assets/background.jpg'))
        ui.draw_title("Credits", (255, 255, 255))
        ui.draw_basic_text("Balance: {}".format(
            self._player.balance), (255, 255, 255), 25, 30, 30)

        ui.draw_centered_basic_text("Developers:", (255, 255, 255), 35, 100)
        ui.draw_basic_text("Quinn Aguiar", (255, 255, 255), 25, 300, 150)
        ui.draw_basic_text("Jacob Duhaime", (255, 255, 255), 25, 750, 150)
        ui.draw_basic_text("Nicholas Faciano", (255, 255, 255), 25, 300, 200)
        ui.draw_basic_text("Grace Gomes", (255, 255, 255), 25, 750, 200)
        ui.draw_basic_text("Harry Grenier", (255, 255, 255), 25, 300, 250)
        ui.draw_basic_text("Emily Hogan", (255, 255, 255), 25, 750, 250)
        ui.draw_basic_text("Leilani Jimenez", (255, 255, 255), 25, 300, 300)
        ui.draw_basic_text("Ben Keeler", (255, 255, 255), 25, 750, 300)
        ui.draw_basic_text("Aidan Kelly", (255, 255, 255), 25, 300, 350)
        ui.draw_basic_text("Tyler Puglia", (255, 255, 255), 25, 750, 350)
        
        ui.draw_centered_basic_text("Attributions:", (255, 255, 255), 35, 400)
        ui.draw_basic_text("MrEliptik", (255, 255, 255), 25, 750, 450)
        ui.draw_basic_text("Yewbi", (255, 255, 255), 25, 750, 500)
        ui.draw_basic_text("Eeve Somepx", (255, 255, 255), 25, 750, 550)
        ui.draw_basic_text("Dave Gandy", (255, 255, 255), 25, 300, 450)
        ui.draw_basic_text("Becris", (255, 255, 255), 25, 300, 500)
        ui.draw_basic_text("Catalin Fertu", (255, 255, 255), 25, 300, 550)
        ui.draw_basic_text("Freepik", (255, 255, 255), 25, 300, 600)

        ui.draw_centered_basic_text("Special thanks to: David H. Brown", (255, 255, 255), 35, 650)

        for button in self._buttons:
            button.draw(self._game.surface)

class Settings(Screen):
    def __init__(self, game: "Game"):
        super().__init__(game)

        self._buttons.extend([
            TextButton(game, (450, game.surface.get_height() - 200),
                       "Reset Balance", 80, ButtonCallbacks.reset_balance(game.player)),
            TextButton(game, (575, game.surface.get_height() - 100), "Exit",
                       80, ButtonCallbacks.return_to_screen(game.screen, game)),
            ImageButton(game, pygame.rect.Rect(game.surface.get_width(
            ) - 100, 30, 50, 50), 'assets/home.png', ButtonCallbacks.load_screen(MainMenu, game)),
            TextButton(game, (495, 150), "-", 100,
                       ButtonCallbacks.update_music_volume(-0.125)),
            TextButton(game, (750, 150), "+", 100,
                       ButtonCallbacks.update_music_volume(0.125)),
            TextButton(game, (495, 300), "-", 100,
                       ButtonCallbacks.update_sfx_volume(-0.125)),
            TextButton(game, (750, 300), "+", 100,
                       ButtonCallbacks.update_sfx_volume(0.125)),

        ])

    def tick(self, event_list: list[pygame.event.Event]):
        for button in self._buttons:
            button.check_for_click(
                filter(lambda event: event.type == pygame.MOUSEBUTTONUP, event_list))

    def handle_input(self):
        ...

    def draw(self, ui: UiBuilder, text_wrapper: WrapText):
        ui.set_background(
            pygame.image.load('assets/background.jpg'))
        ui.draw_title("Settings", (255, 255, 255))
        ui.draw_basic_text("Balance: {}".format(
            self._player.balance), (255, 255, 255), 25, 30, 30)

        ui.draw_centered_basic_text("Music Volume", (255, 255, 255), 40, 135)
        for music_volume_bar_index in range(0, 8):
            colored = audio.music_volume > music_volume_bar_index / 8
            color_rgb = (100, 200, 100) if colored else (127, 127, 127)
            ui.draw_rect(545 + (music_volume_bar_index * 25),
                         185 - (music_volume_bar_index * 2.5),
                         10,
                         20 + (music_volume_bar_index * 6),
                         color_rgb)

        ui.draw_centered_basic_text("SFX Volume", (255, 255, 255), 40, 285)
        for sfx_volume_bar_index in range(0, 8):
            colored = audio.sfx_volume > sfx_volume_bar_index / 8
            color_rgb = (100, 200, 100) if colored else (127, 127, 127)
            ui.draw_rect(545 + (sfx_volume_bar_index * 25),
                         335 - (sfx_volume_bar_index * 2.5),
                         10,
                         20 + (sfx_volume_bar_index * 6),
                         color_rgb)

        for button in self._buttons:
            button.draw(self._game.surface)


class Instructions(Screen):
    def __init__(self, game: "Game", description):
        super().__init__(game)
        self.description = description

        self._buttons.extend([
            TextButton(game, (575, game.surface.get_height() - 100), "Exit",
                       80, ButtonCallbacks.return_to_screen(game.screen, game)),
        ])

    def tick(self, event_list: list[pygame.event.Event]):
        for button in self._buttons:
            button.check_for_click(
                filter(lambda event: event.type == pygame.MOUSEBUTTONUP, event_list))

    def handle_input(self):
        ...

    def draw(self, ui: UiBuilder, text_wrapper: WrapText):
        ui.set_background(
            pygame.image.load('assets/background.jpg'))
        ui.draw_title("Instructions", (255, 255, 255))
        ui.draw_basic_text("Balance: {}".format(
            self._player.balance), (255, 255, 255), 25, 30, 30)

        text_wrapper.draw_wrapped_text(self.description, (255, 255, 255),
                           30, 100, 100)

        for button in self._buttons:
            button.draw(self._game.surface)

class GameOver(Screen):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self._buttons.extend([
            ImageButton(game, pygame.rect.Rect(game.surface.get_width(
            ) - 100, 30, 50, 50), 'assets/home.png', ButtonCallbacks.load_screen(MainMenu, game)),
        ])
        # Prevents screen from appearing instantaneously after the player's losing move
        pygame.time.wait(500)
        audio.play(audio.Sounds.game_over)
       
    
    def tick(self, event_list: list[pygame.event.Event]):
        for button in self._buttons:
            button.check_for_click(
                filter(lambda event: event.type == pygame.MOUSEBUTTONUP, event_list))

    def handle_input(self):
        ...
    
    def draw(self, ui: UiBuilder, text_wrapper: WrapText):
        ui.set_background(
            pygame.image.load('assets/background.jpg'))
        ui.draw_centered_basic_text("Game Over!", (255, 255, 255), 120, 300)
        ui.draw_centered_basic_text("Better luck next time...", (255, 255, 255), 60, 400)

        for button in self._buttons:
            button.draw(self._game.surface)
