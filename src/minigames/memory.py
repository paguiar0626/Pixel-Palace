from typing import TYPE_CHECKING

import pygame

from button import ButtonCallbacks, ImageButton, TextButton
from card import Card
from deck import Deck
from hud_builder import HUDBuilder
from screen import Screen
from ui_builder import UiBuilder
from read_txtfile import WrapText

if TYPE_CHECKING:
    from game import Game
    from player import Player


class Memory(Screen):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self._card_rows = 4
        self._card_cols = 4
        self._deck = Deck("memory")
        self._matches: list[Card] = []
        self._turns_elapsed = 0
        self._game_over = False
        self._card_draw_options = {
            "scale_factor": 2.0,
            "x_spacing": 200,
            "x_offset": 275,
            "y_spacing": 150,
            "y_offset": 75,
        }
        self._card_buttons: list[ImageButton] = []

        self._buttons.extend(HUDBuilder.get_hud_buttons(game, "memory"))

        self._deck.shuffle()

        for i, card in enumerate(self._deck.deck):
            x = ((i // 4) * self._card_draw_options["x_spacing"]) \
                + self._card_draw_options["x_offset"]
            y = ((i % 4) * self._card_draw_options["y_spacing"]) \
                + self._card_draw_options["y_offset"]

            self._card_buttons.append(
                ImageButton(self._game, pygame.rect.Rect(
                            x, y,
                            card.CARD_SS_WIDTH *
                            self._card_draw_options["scale_factor"],
                            card.CARD_SS_HEIGHT * self._card_draw_options["scale_factor"]),
                            "assets/invisible.png", ButtonCallbacks.flip_card_face_up(card))
            )

    def tick(self, event_list: list[pygame.event.Event]):
        if self._game_over:
            player = self._game.player
            payout = self._calculate_payout(player.bet, self._turns_elapsed, self._card_rows * self._card_cols / 2)
            player.balance += payout
            self._game.screen = MemoryGameOver(self._game, payout, player.balance)
            return
        
        if len(self._matches) == len(self._deck.deck):
            self._game_over = True

        flipped_cards = [
            card for card in self._deck.deck if card.is_face_up and card not in self._matches]

        if len(flipped_cards) == 2:
            card_a = flipped_cards[0]
            card_b = flipped_cards[1]

            if card_a.id == card_b.id:
                self._matches.extend([card_a, card_b])
            else:
                pygame.time.wait(1000)
                card_a.flip()
                card_b.flip()

            self._turns_elapsed += 1

        for button in (self._buttons + self._card_buttons):
            button.check_for_click(
                filter(lambda event: event.type == pygame.MOUSEBUTTONUP, event_list))

    def handle_input(self):
        ...

    def draw(self, ui: UiBuilder, text_wrapper: WrapText):
        ui.set_background(pygame.image.load('assets/background.jpg'))

        ui.draw_basic_text(f"Turns elapsed: {self._turns_elapsed}", (255, 255, 255), 30, 10, 10)
        ui.draw_basic_text(f"Current payout: {self._calculate_payout(self._game.player.bet, self._turns_elapsed, self._card_rows * self._card_cols / 2)}",
                            (255, 255, 255), 30, 10, 40)


        for i, card in enumerate(self._deck.deck):
            x = (
                (i // 4) * self._card_draw_options["x_spacing"]) + self._card_draw_options["x_offset"]
            y = (
                (i % 4) * self._card_draw_options["y_spacing"]) + self._card_draw_options["y_offset"]
            card.draw(
                self._card_draw_options["scale_factor"], self._game.surface, x, y)  # type: ignore

        for button in self._buttons:
            button.draw(self._game.surface)

    def _calculate_payout(self, initial_bet: int, turns_elapsed: int, grace_limit: int):
        # negative exponential equation
        payout = initial_bet * 4 - 1.75 ** max((turns_elapsed - grace_limit), 0) + 1
        return max(round(payout), 0)
        

class MemorySetup(Screen):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self._buttons.extend(HUDBuilder.get_hud_buttons(game,"memory"))
        self._buttons.extend(HUDBuilder.get_bet_buttons(game))
        self._buttons.extend([
            TextButton(game, (550, 475), "- Start -", 60, ButtonCallbacks.load_screen(Memory, game)),
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
        
        ui.draw_title("Set Your Bet!", (255, 255, 255))
        ui.draw_centered_basic_text(f"Available funds: {self._game.player.balance}", (255, 255, 255), 40, 300)
        ui.draw_centered_basic_text(f"Bet: {self._game.player.bet}", (255, 255, 255), 50, 350)

        for button in self._buttons:
            button.draw(self._game.surface)

class MemoryGameOver(Screen):    
    def __init__(self, game: "Game", payout: int, balance: int):
        from menus import MainMenu
        
        super().__init__(game)
        self._payout = payout
        self._balance = balance
        self._buttons.extend([
            TextButton(game, (550, 475), "- Exit -", 60, ButtonCallbacks.load_screen(MainMenu, game)),
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
        
        ui.draw_title("You matched every card!", (255, 255, 255))
        ui.draw_centered_basic_text(f"You won: {self._payout}", (255, 255, 255), 40, 300)
        ui.draw_centered_basic_text(f"Your new balance: {self._balance}", (255, 255, 255), 50, 350)

        for button in self._buttons:
            button.draw(self._game.surface)
