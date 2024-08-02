from typing import Text
import pygame

from spritesheet import Spritesheet
from texture import Texture

# these might move into deck eventually
standard_values = ["A", "2", "3", "4", "5",
                   "6", "7", "8", "9", "T", "J", "Q", "K"]
standard_suits = ["C", "H", "S", "D"]

card_ids = []
for value in standard_values:
    for suit in standard_suits:
        card_ids.append(value + suit)


class Card:
    def __init__(self, id: str, is_face_up=True):
        # set standard width and height based on spritesheet
        self.CARD_SS_WIDTH = 32.0
        self.CARD_SS_HEIGHT = 48.0
        self.is_face_up = is_face_up
        self.sprite: pygame.surface.Surface

        # don't allow adding cards not in standard deck
        if id[0] in standard_values and id[1] in standard_suits:
            self.id = id
            self.num = id[0]
            self.suit = id[1]
        else:
            raise ValueError(f"Card {id} not in deck")

        if self.suit == "C" or self.suit == "S":
            self.color = "black"
        else:
            self.color = "red"

        # set textures
        texture = Texture("assets/pixel_playing_cards/Pixel_Playing_Card_Set_YEWBI.png", "default_coordinates.csv")
        dict = texture.coordinates
        self._front_sprite = texture.images.image_at(pygame.Rect(
            float(dict[self.id][0]), float(dict[self.id][1]), self.CARD_SS_WIDTH, self.CARD_SS_HEIGHT))
        self._back_sprite = texture.images.image_at(pygame.Rect(
            float(dict["B"][0]), float(dict["B"][1]), self.CARD_SS_WIDTH, self.CARD_SS_HEIGHT))
        
    def values_as_ints(self, ace: str):
        """Convert the value strings to integers so they can be compared to one another.\n
        ARGS:
        ace: 'high' or 'low' for how to compare the Ace"""
        match self.num:
            case "2":
                self.num = 2
                return
            case "3":
                self.num = 3
                return
            case "4":
                self.num = 4
                return
            case "5":
                self.num = 5
                return
            case "6":
                self.num = 6
                return
            case "7":
                self.num = 7
                return
            case "8":
                self.num = 8
                return
            case "9":
                self.num = 9
                return
            case "T":
                self.num = 10
                return
            case "J":
                self.num = 11
                return
            case "Q":
                self.num = 12
                return
            case "K":
                self.num = 13
                return
            case "A":
                if ace is 'high':
                    self.num = 14
                    return
                elif ace is 'low':
                    self.num = 1
                    return
                else:
                    raise ValueError(f"Enter 'high' or 'low', not {ace}")
                


    # pick the specific face from the spritesheet
    def set_front_texture(self, spritesheet_str: str):
        x = float(Card.coordinates[self.id][0])
        y = float(Card.coordinates[self.id][1])
        spritesheet = Spritesheet(spritesheet_str)
        self.front_sprite = spritesheet.image_at(
            pygame.Rect(x, y, self.CARD_SS_WIDTH, self.CARD_SS_HEIGHT))

    # all back textures will be the same
    def set_back_texture(self, spritesheet_str: str):
        x = float(Card.coordinates["B"][0])
        y = float(Card.coordinates["B"][1])
        spritesheet = Spritesheet(spritesheet_str)
        self.back_sprite = spritesheet.image_at(
            pygame.Rect(x, y, self.CARD_SS_WIDTH, self.CARD_SS_HEIGHT))


    def draw(self, scale_amt: float, surface: pygame.surface.Surface, x: int, y: int, rotated = 0 ):
        """set face sprite and then draw"""
        if self.is_face_up:
            self.sprite = pygame.transform.scale(self._front_sprite, ((
                self.CARD_SS_WIDTH*scale_amt), (self.CARD_SS_HEIGHT*scale_amt)))
        else:
            self.sprite = pygame.transform.scale(
                self._back_sprite, ((self.CARD_SS_WIDTH*scale_amt), (self.CARD_SS_HEIGHT*scale_amt)))
        surface.blit(self.sprite, (x, y))


        if rotated != 0:
                self.sprite = pygame.transform.rotate(self.sprite, rotated)
                surface.blit(self.sprite, (x, y))

    def flip(self):                                   # swap sprite
        if self.is_face_up:
            self.is_face_up = False
        else:
            self.is_face_up = True
