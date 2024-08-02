import pygame
from game import Game


def main():
    pygame.display.set_caption("Pixel Palace")
    pygame.display.set_icon(pygame.image.load("assets/window_icon.png"))
    width = 1280
    height = 720
    surface = pygame.display.set_mode((width, height))
    pygame.font.init()
    pygame.mixer.init()
    game = Game(width, height, surface)
    game.start()


if __name__ == "__main__":
    main()
