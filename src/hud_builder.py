from typing import TYPE_CHECKING

import pygame

# Prevents circular import
if TYPE_CHECKING:
    from button import Button
    from game import Game


class HUDBuilder():
    @staticmethod
    def get_hud_buttons(game: "Game", currentScreen) -> list["Button"]:
        from button import ButtonCallbacks, ImageButton
        from read_txtfile import ReadInstructions
        from menus import Instructions, Settings

        instructions = ReadInstructions("info_texts/" + currentScreen + "_info.txt")

        return [
            ImageButton(game, pygame.rect.Rect(game.surface.get_width() - 100, game.surface.get_height() -
                        75, 50, 50), 'assets/settings.png', ButtonCallbacks.load_screen(Settings, game)),
            ImageButton(game, pygame.rect.Rect(game.surface.get_width() - 175, game.surface.get_height() - 75, 50, 50),
                        'assets/instructions.png', ButtonCallbacks.load_screen(Instructions, game, instructions.get_contents())),
        ]
    
    @staticmethod
    def get_bet_buttons(game: "Game") -> list["Button"]:
        from button import ButtonCallbacks, ImageButton

        return[
            ImageButton(game, pygame.rect.Rect(game.surface.get_width(
            ) / 2 - 200, game.surface.get_height() - 75, 50, 50), 'assets/left_two.png', ButtonCallbacks.update_bet(game.player, -10)),
            ImageButton(game, pygame.rect.Rect(game.surface.get_width(
            ) / 2 - 100, game.surface.get_height() - 75, 50, 50), 'assets/left_one.png', ButtonCallbacks.update_bet(game.player, -1)),
            ImageButton(game, pygame.rect.Rect(game.surface.get_width(
            ) / 2 + 100, game.surface.get_height() - 75, 50, 50), 'assets/right_one.png', ButtonCallbacks.update_bet(game.player, 1)),
            ImageButton(game, pygame.rect.Rect(game.surface.get_width(
            ) / 2 + 200, game.surface.get_height() - 75, 50, 50), 'assets/right_two.png', ButtonCallbacks.update_bet(game.player, 10))
        ]
