import pygame

from card import Card

pygame.init()

WIDTH = 1280
HEIGHT = 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# create a specific instance of a card to test on
# testing if picking a specific card works
king_diamond = Card("KD")

is_running = True
while is_running:
    WINDOW.fill((231, 171, 154))
    # scale the card up since the original is so small
    king_diamond.draw(4.0, WINDOW, 100, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:      # card flip is triggered by spacebar
                king_diamond.flip()

    pygame.display.update()
