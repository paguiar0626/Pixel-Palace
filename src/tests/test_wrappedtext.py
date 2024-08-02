from read_txtfile import WrapText
from unittest import mock
import pytest
import pygame

def test_make_lines_function():
    instance = WrapText(None, None, None)
    pygame.font.init() # initialize pygame fonts

    # Test that a single word is wrapped correctly
    text = "cards"
    main_font = pygame.font.Font(None, 20)
    expected_output = ["cards"]
    assert instance.make_lines(text, main_font) == expected_output

    # Test that a sentence is wrapped correctly
    text = "I love card and coin based casino games"
    main_font = pygame.font.Font(None, 20)
    expected_output = ["I love card and coin based casino games"]
    assert instance.make_lines(text, main_font) == expected_output

    # Test that long words are handled correctly
    text = "asdfghjklasdfghjklasdfghjklasdfghjkl"
    main_font = pygame.font.Font(None, 20)
    expected_output = ["asdfghjklasdfghjklasdfghjklasdfghjkl"]
    assert instance.make_lines(text, main_font) == expected_output

    # Test that text is split into multiple lines when it exceeds the width of the textbox
    text = "Welcome to the Pixel Casino! Here you can play a variety of card and coin based games. You will begin with a balance of 1000 coins that you may use to bet inside each game. Each time you lose a bet, you will lose the amount you set. Each time you win a bet, you will win double the amount you set. Your overall balance will not reset unless you do so manually inside the settings menu. There you may also adjust the music and sound effect levels. Please make a game selection to begin. There are further instructions inside each of the games."
    main_font = pygame.font.Font(None, 20)
    expected_output = ['Welcome to the Pixel Casino! Here you can play a variety of card and coin based games. You will begin with a balance of 1000 coins that you may use to bet', 'inside each game. Each time you lose a bet, you will lose the amount you set. Each time you win a bet, you will win double the amount you set. Your overall', 'balance will not reset unless you do so manually inside the settings menu. There you may also adjust the music and sound effect levels. Please make a', 'game selection to begin. There are further instructions inside each of the games.']
    assert instance.make_lines(text, main_font) == expected_output