import random
from typing import TYPE_CHECKING

import pygame

from hud_builder import HUDBuilder
from screen import Screen
from timer import Timer
from ui_builder import UiBuilder
from button import TextButton, ButtonCallbacks
from read_txtfile import WrapText

if TYPE_CHECKING:
    from game import Game

class CoinFlip(Screen):

    def __init__(self, game: "Game"):
        super().__init__(game)

        self._timer = Timer()
        self._timer.start()

        self._timer = Timer()
        self._timer.start()

        self._timer = Timer()
        self._timer.start()

        self._game = game
        self._player = game.player
        self._bet = self._player.bet
        self._bet_size = 1
        self._outcome = ""

        self._buttons.extend(HUDBuilder.get_hud_buttons(game, "coin_flip"))
        self._buttons.extend(HUDBuilder.get_bet_buttons(game))

        self._buttons.extend([
            TextButton(game, (game.surface.get_width()/2 - 200, 100), "Heads",
                       80, ButtonCallbacks.set_CF_bet_heads(self._player)),
            TextButton(game, (game.surface.get_width()/2 + 100, 100), "Tails",
                       80, ButtonCallbacks.set_CF_bet_tails(self._player)),
        ])

    def tick(self, event_list: list[pygame.event.Event]):

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP and self.flip_coin_button.collidepoint(event.pos):
                if self._player.choice:
                    self.flip_coin()
                    self.alter_balance()

        if (self._player.balance <= 0):
            from menus import GameOver

            self._game.screen = GameOver(self._game)
            return
        
        for button in self._buttons:
            button.check_for_click(
                filter(lambda event: event.type == pygame.MOUSEBUTTONUP, event_list))
    
    def handle_input(self):
        ...

    def draw(self, ui: UiBuilder, text_wrapper: WrapText):
        self.flip_coin_button = pygame.Rect(0, 0, 0, 0)

        ui.set_background(
            pygame.image.load('assets/background.jpg'))

        # text
        if (not self._outcome):
            ui.draw_basic_text(
                "Select one:", (255, 255, 255), 70, 500, 30)
        else:
            ui.draw_basic_text(
                self._outcome, (255, 255, 255), 70, self._game.surface.get_width()/2 -50, 30)

        height_base_value = 80
        ui.draw_basic_text(
            "Info", (255, 255, 255), 40, 30, height_base_value-50)

        ui.draw_basic_text(f"Balance: {self._player.balance}",
                           (255, 255, 255), 25, 30, height_base_value)

        ui.draw_basic_text(f"Bet$: {self._player.bet}", (255, 255, 255),
                           25, 30, height_base_value+40)

        ui.draw_basic_text(f"Selection: {self._player.choice}", (255,
                                                             255, 255), 25, 30, height_base_value+80)

        ui.draw_basic_text(f"Time elapsed: {self._timer.time_elapsed_string()}", (
            255, 255, 255), 25, 30, self._game.surface.get_height() - 75)

        self.flip_coin_button = ui.place_image(pygame.image.load(
            f'assets/{self._outcome if self._outcome else "heads"}.png'), 200, 200, self._game.surface.get_width()/2 - 75, 310)

        for button in self._buttons:
            button.draw(self._game.surface)

    def flip_coin(self):
        self._outcome = random.choice(("heads", "tails"))

    def alter_balance(self):
        if self._outcome == self._player.choice:
            self._player.balance += self._player.bet * 2
        else:
            self._player.balance -= self._player.bet

    def timer_expired(self):
        self._outcome = "Time's up!"
        self.flip_coin()
        self.alter_balance()
