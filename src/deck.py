import random

from card import Card, card_ids
import random


class Deck:
    def __init__(self, type="default", memory_sets=8, memory_difficulty=2):
        """ARGS:
        type: 'default', 'memory', or 'empty'
        memory_sets (for type='memory'): the number of sets to generate
        memory_difficulty (for type='memory'): the number of copies of each unique card
        """
        self.deck: list[Card] = []

        if type == "default":
            for id in card_ids:
                new_card = Card(id)
                self.deck.append(new_card)
        elif type == "memory":
            singles = random.sample(card_ids, memory_sets)
            for single in singles:
                for i in range(memory_difficulty):
                    new_card = Card(single, False)
                    self.deck.append(new_card)
        elif type == "empty":
            pass
        else:
            raise ValueError(f"Invalid deck type {type}")

    def size(self) -> int:
        """Return the number of cards in this Deck"""
        return len(self.deck)

    def shuffle(self):
        """Shuffles the deck"""
        random.shuffle(self.deck)

    def copy_deck(self, times: int = 1):
        """Creates the specified number of copies of this deck.  Returns as a list of Decks.\n
        ARGS:
        times: The number of copies to make.  Defaults to 1."""
        original = self.deck
        new_decks = []
        for _ in range(times):
            new = Deck("empty")
            new.deck.extend(original)
            new_decks.append(new)
        return new_decks
            

    def combine(self, other: list[list[Card]]):
        """Add other decks into this deck.\n
        ARGS:
        other: a list of Decks to add into this one"""
        for deck in other:
            for card in deck.deck:
                self.add_card_bottom(card)

    def convert_all_values(self, ace: str):
        """Convert the value of every card in the deck to an integer\n
        ARGS:
        ace (str): 'high' or 'low' for how to compare the ace"""
        for card in self.deck:
            card.values_as_ints(ace)

    def deal_top(self) -> Card:
        """Deals the top card from the Deck."""
        return self.deck.pop(0)

    def add_card_top(self, to_add: Card):
        """Adds a Card to the top of the Deck.\n
        ARGS:
        to_add: the Card to add"""
        self.deck.insert(0, to_add)
    
    def add_card_bottom(self, to_add: Card):
        """Adds a Card to the bottom of the Deck.\n
        ARGS:
        to_add: the Card to add"""
        self.deck.append(to_add)

    def add_card(self, to_add: Card, top_or_bot): # Doesn't follow the SRP but im keeping this around so I dont break people's code
        """Use add_card_top or add_card_bottom instead of this method."""
        if (top_or_bot == 'B'):
            self.deck.append(to_add)
        elif (top_or_bot == 'T'):
            self.deck.insert(0, to_add)
        else:
            raise ValueError(f"Enter 'T' or 'B', not {top_or_bot}")
class GameHand(Deck):
    """Constructor to set a default deck with a shuffle before we assign any cards"""

    def __init__(self):
        super().__init__(type="default", memory_sets=8, memory_difficulty=2)
        self.game_hand = Deck("empty")

        """ Function to add a card to a player hand """

    def add_card(self, card):
        self.game_hand.add_card_top(card)

        """ Function to clear the hand (back to an empty list) """

    def clear_hand(self):
        self.game_hand.clear()

        """ Function to return the number of cards in the hand"""

    def num_cards(self):
        num = self.game_hand.size()
        return num

        """Function to return the top card of the hand"""

    def top_card(self):
        top = self.game_hand[(len(self.game_hand) - 1)]
        return top
