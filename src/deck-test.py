import pygame

from deck import Deck

pygame.init()

WIDTH = 1280
HEIGHT = 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

default_deck = Deck()

memory_deck = Deck("memory", 8, 4)

expand_test = Deck("empty")
expand_test.combine([default_deck])

copy_test = default_deck.copy_deck()[0]

is_running = True
while is_running:
    WINDOW.fill((145, 185, 220))

    for i, card in enumerate(copy_test.deck):
        x = ((i // 4) * 75) + 100
        y = ((i % 4) * 105) + 50
        card.draw(1.5, WINDOW, x, y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    pygame.display.update()
