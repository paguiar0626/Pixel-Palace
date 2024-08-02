from typing import TYPE_CHECKING
import pygame
from player import Player,Dealer
from screen import Screen
from card import Card
from deck import Deck
from ui_builder import UiBuilder
from button import ButtonCallbacks, ImageButton, TextButton
from texture import Texture
from hud_builder import HUDBuilder
from read_txtfile import WrapText

# Prevents circular import
if TYPE_CHECKING:
    from game import Game

class BlackJack(Screen):
    """
    This class represents the BlackJack game screen and handles the game logic and user interactions. It is a subclass of the Screen class and inherits its attributes and methods.

    Attributes:
    _player (Player): The player object representing the user.
    _dealer (Dealer): The dealer object representing the computer-controlled dealer.
    WHITE (tuple): A tuple representing the color white in RGB format.
    _player_total (int): The current total value of the player's hand.
    _dealer_total (int): The current total value of the dealer's hand.
    _dealer_blackjack (int): A flag indicating whether the dealer has a blackjack (1) or not (0).
    _player_blackjack (int): A flag indicating whether the player has a blackjack (1) or not (0).
    _dealer_bust (int): A flag indicating whether the dealer has busted (1) or not (0).
    _player_bust (int): A flag indicating whether the player has busted (1) or not (0).
    _bet_amount (int): The current bet amount of the player.
    _Double_selected (int): A flag indicating whether the "Double" action has been selected (1) or not (0).
    _first_Tick (int): A flag indicating whether it's the first tick of the game loop (1) or not (0).
    _current_screen (str): The current screen being displayed.
    _bet_mutiplier (int): The current bet multiplier.
    _dealer_card_pos (tuple): A tuple representing the dealer's card position on the screen.
    _Player_card_pos (tuple): A tuple representing the player's card position on the screen.
    _outcome (str): A string describing the outcome of the game.
    _buttons (list): A list of ImageButton objects representing various on-screen buttons.

    Methods:
    click_settings(self: ImageButton): Changes the current screen to the Settings screen.
    click_instructions(self: ImageButton): Changes the current screen to the Instructions screen.
    
    """
    def __init__(self, game: "Game",):
        super(BlackJack,self).__init__(game)
        self._player = game.player
        self._dealer = Dealer()
        self.WHITE = (255,255,255)
        self._player_total = 0
        self._dealer_total = 0
        self._dealer_blackjack = 0
        self._player_blackjack = 0
        self._dealer_bust = 0
        self._player_bust = 0
        self._bet_amount = 1
        self._Double_selected = 0
        self._first_Tick = 1
        self._buttons.extend(HUDBuilder.get_hud_buttons(game, "blackjack"))
        self.reset_deck()
        self._current_screen = "Defult"
        self._bet_mutiplier = 1
        self._dealer_card_pos = (600, 10)
        self._Player_card_pos = (600,500)
        self._outcome = ""
    # Creates the settings button and allows you to goto the settings

# Logic ->
########################################################################################################################################

# Deal cards to the player and the dealer (When the game is started call this function first)
    def deal_cards(self):
        self._player._hand, self._dealer._hand = [self._deck.deal_top() for _ in range(2)], [self._deck.deal_top() for _ in range(2)]
        # Update player's total
        self._player_total = self._calculate_hand_value(self._player.hand)
        # Update dealer's total
        self._dealer_total = self._calculate_hand_value(self._dealer.hand)
        # Check for player blackjack
        if self._is_blackjack(self._player.hand):
           #print("Player has blackjack. Automatically standing.")
           self._player_blackjack = 1
           self.stand()
        else:
            pass
        if self._is_blackjack(self._dealer.hand):
           self._dealer_blackjack = 1
        else:
            pass

# This takes the top card of the deck and adds it to the players hand
    def hit(self):
        new_card = self._deck.deal_top()
        self._player.hand.append(new_card)
        self._player_total = self._calculate_hand_value(self._player.hand)

# We double the bet and only allow the user that last hit
    def double(self):
        self._Double_selected = 1
        self._bet_amount *= 2
        self.hit()







    def stand(self):
    # dealer's turn
        while self._dealer_total < 17:
            new_card = self._deck.deal_top()  # Draw a card from the deck
            self._dealer.hand.append(new_card)  # Add the card to the dealer's hand
            self._dealer_total = self._calculate_hand_value(self._dealer.hand)  # Update dealer's total

        

        if self._player_bust == 1 or self._player_total > 21:
            self._outcome = "player_bust"

        if self._dealer_total > 21:
            self._dealer_bust = 1

        if self._dealer_blackjack == 1:
            self._outcome = "dealer_blackjack"

        if self._outcome == "dealer_blackjack" or self._outcome == "player_blackjack" or self._outcome == "player_bust":
            pass
        else:
            if self._player_total > self._dealer_total:
                self._outcome = "player_win"
            elif (self._player_total == self._dealer_total):
                self._outcome = "push"
            elif self._dealer_bust == 1 and self._player_bust == 0:
                self._outcome = "dealer_bust"
            else:
                self._outcome = "dealer_win"

        self.update_balance(self._outcome)
        self._current_screen = "After_Game"
        print(self._outcome)


    def bet(self, amount) -> bool:
        if amount > 0 and amount <= self._player.balance:
            self._player.balance -= amount
            self._bet_amount = amount
            return True
        else:
            # Invalid bet amount or not enough funds to place the bet
            return False






    def _is_blackjack(self, hand) -> bool:
        ace_present = False
        ten_point_card_present = False
        for card in hand:
            card_value = self._get_card_value(card)
            if card_value == 11:
               ace_present = True
            if card_value == 10:
               ten_point_card_present = True
        if ace_present and ten_point_card_present:
           return True
        else:
            return False

# Gets the Numarical value of a card
    def _get_card_value(self, card: Card) -> int:
        rank = card.num
        if rank.isdigit():
            return int(rank)
        elif rank == "A":
            return 11  # We Handle the aces within the game logic
        else:
            return 10

# We use this function to calculate the whole hand
    def _calculate_hand_value(self, hand: Player) -> int:
        value = 0
        aces = 0
        for card in hand:
            card_value = self._get_card_value(card)
            if card_value == 11:
                aces += 1
            value += card_value

        for _ in range(aces):
            if value > 21:
                value -= 10

        return value

# Pays out the player
    def update_balance(self, outcome):
        if outcome == "player_win" or outcome == "dealer_bust":
            self._player.balance += self._bet_amount * 2
        elif outcome == "player_blackjack":
            self._player.balance += int(self._bet_amount * 2.5)
        elif outcome == "push":
            self._player.balance += self._bet_amount
        # No need for an else clause since the balance should not be updated for other outcomes

# Generates a new drkc and shuffles it
    def reset_deck(self):
        self._deck = Deck()  # Create a new deck
        self._deck.shuffle()  # Shuffle the new deck

# Resets all values to defult for the next game
    def reset_game(self):
    # Clear player's and dealer's hands
        self._player._hand.clear()
        self._dealer._hand.clear()
    
    # Reset player's and dealer's total
        self._player_total = 0
        self._dealer_total = 0
    
    # Reset player's and dealer's flags
        self._dealer_blackjack = 0
        self._player_blackjack = 0
        self._dealer_bust = 0
        self._player_bust = 0
        
    
    # Reset the bet amount and the total bet amount
        self._bet_amount = 1
    
    # Reset the bet multiplier
        self._bet_mutiplier = 1
    
    # Reset the outcome
        self._outcome = ""
    # Resets trackers
        self._first_Tick = 1
        self._Double_selected = 0
    # Shuffle the deck
        self.reset_deck()








#UI ->
###################################################################################################################################

# Screen Creations

    def Defult_Screen(self, ui: UiBuilder):
        ui.set_background(pygame.image.load('assets/background.jpg'))
        ui.draw_centered_basic_text('Balance: {}'.format(str(self._player.balance)),self.WHITE, 50, 25)
        ui.draw_basic_text('Bet: {}'.format(str(self._bet_amount)), self.WHITE, 100,100, 50)
        ui.draw_basic_text('Bet X: {}X'.format(str(self._bet_mutiplier)), self.WHITE, 100,100, 175)
        self.start_button = ui.place_image(pygame.image.load('assets/start_buton.png'), 500, 250, 675, 325)

        #bet
        ui.draw_basic_text("   Bet   ", self.WHITE, 100, 200, 375)
        self.bet_up_button = ui.place_image(pygame.image.load('assets/bet_up_arrow.png'), 100, 100, 350, 375)
        self.bet_down_button = ui.place_image(pygame.image.load('assets/bet_down_arrow.png'), 100, 100, 50, 375)
        

        #bet increse 
        ui.draw_basic_text(" Bet X ", self.WHITE, 100, 150, 550)
        self.betX_up_button = ui.place_image(pygame.image.load('assets/bet_up_arrow.png'), 100, 100, 350, 550)
        self.betX_down_button = ui.place_image(pygame.image.load('assets/bet_down_arrow.png'), 100, 100, 50, 550)

    def Main_Game(self, ui: UiBuilder) -> UiBuilder:
        def static_display():
            ui.Back_Card(self._dealer.hand[0])
            ui.set_background(pygame.image.load('assets/background.jpg'))
            ui.draw_basic_text('Bet: {}'.format(str(self._bet_amount)), self.WHITE, 50, 25, 0)
            ui.draw_basic_text('Balance: {}'.format(str(self._player.balance)), self.WHITE, 50, 25, 50)
            ui.draw_basic_text('Player Total: {}'.format(str(self._player_total)), self.WHITE, 50, 300, 600)
            Hit_button = ui.place_image(pygame.image.load('assets/button_picture.png'), 200, 100, 850, 600)
            Stand_button = ui.place_image(pygame.image.load('assets/button_picture.png'), 200, 100, 50, 600)
            ui.draw_basic_text('Hit', self.WHITE, 50, 925, 625)
            ui.draw_basic_text('Stand', self.WHITE, 50, 100, 625)
            return Hit_button, Stand_button

        
        self.Hit_button, self.Stand_button = static_display()
        if len(self._player.hand) == 2:
            self.Double_Button = ui.place_image(pygame.image.load('assets/button_picture.png'), 200, 100, 50, 500)
            ui.draw_basic_text('Double', self.WHITE, 50, 100, 525)

        ui.Display_cards(self._dealer.hand,self._dealer_card_pos,"dealer")
        ui.Display_cards(self._player.hand,self._Player_card_pos,"player",self._Double_selected)


        
        if self._dealer_blackjack == 1 and self._player_blackjack == 0:
            self._outcome = "dealer_blackjack"
        if self._dealer_blackjack == 0 and self._player_blackjack == 1:
            self._outcome == "player_blackjack"
            self.stand()
        
        if self._player_total >= 21:
            if self._player_total > 21:
                self._player_bust = 1
            self.stand()

    def After_Game(self,ui: UiBuilder):
        ui.Front_Card(self._dealer.hand[0])
        ui.set_background(pygame.image.load('assets/background.jpg'))
        ui.draw_basic_text('Bet: {}'.format(str(self._bet_amount)), self.WHITE, 50, 25, 0)
        ui.draw_basic_text('Balance: {}'.format(str(self._player.balance)), self.WHITE, 50, 25, 50) 
        ui.draw_basic_text('Player Total: {}'.format(str(self._player_total)), self.WHITE, 50, 300, 600)

        
        ui.Display_cards(self._player.hand,self._Player_card_pos,"player",self._Double_selected)
        if self._first_Tick == 1:
            ui.Delay_Display_cards(self._dealer.hand,self._dealer_card_pos)
        else:
            ui.Display_cards(self._dealer.hand,self._dealer_card_pos,"dealer")

        ui.draw_basic_text('Dealer Total: {}'.format(str(self._dealer_total)), self.WHITE, 50, 800, 10)
        ui.draw_basic_text('Outcome: {}'.format(str(self._outcome)), self.WHITE, 50, 25, 100)
        self.play_again_button = ui.place_image(pygame.image.load('assets/play_again.png'), 400, 200, 500, 250)
        self._first_Tick = 0

# Main Game functions

    def tick(self, event_list: list[pygame.event.Event]):
        for event in event_list:
            if self._current_screen == "Defult":

                if event.type == pygame.MOUSEBUTTONUP and self.start_button.collidepoint(event.pos):
                    # Call the bet function with the total bet amount
                    if self.bet(self._bet_amount):
                        self._current_screen = "Main_Game"
                        self.deal_cards()
                    else:
                        print("Failed to place the bet.")
                #bet x
                if event.type == pygame.MOUSEBUTTONUP and self.betX_up_button.collidepoint(event.pos):
                    if (self._bet_mutiplier * 10) < self._player.balance:
                        self._bet_mutiplier *= 10

                if event.type == pygame.MOUSEBUTTONUP and self.betX_down_button.collidepoint(event.pos):
                    if (self._bet_mutiplier // 10) > 0:
                        self._bet_mutiplier = self._bet_mutiplier // 10


                #bet

                if event.type == pygame.MOUSEBUTTONUP and self.bet_up_button.collidepoint(event.pos):
                    if (self._bet_amount + self._bet_mutiplier) < self._player.balance:
                        self._bet_amount += self._bet_mutiplier
                    else:
                        pass

                    
                if event.type == pygame.MOUSEBUTTONUP and self.bet_down_button.collidepoint(event.pos):
                    if ((self._bet_amount - self._bet_mutiplier) > 0):
                        self._bet_amount -= self._bet_mutiplier

            if self._current_screen == "Main_Game":
                try:
                    if event.type == pygame.MOUSEBUTTONUP and self.Hit_button.collidepoint(event.pos):
                        if self._player_total < 21:
                            self.hit()
                        else:
                            pass
                except:
                    pass
                try:
                    if event.type == pygame.MOUSEBUTTONUP and self.Stand_button.collidepoint(event.pos):
                        self.stand()
                except:
                    pass
                try:
                    if event.type == pygame.MOUSEBUTTONUP and self.Double_Button.collidepoint(event.pos):
                        if self.bet(self._bet_amount):
                            self.double()
                            if self._player_total >= 21:
                                if self._player_total > 21:
                                    self._player_bust = 1
                            self.stand()
                        else:
                            pass
                except:
                    pass
            if self._current_screen == "After_Game":
                try:
                    if event.type == pygame.MOUSEBUTTONUP and self.play_again_button.collidepoint(event.pos):
                        # Reset game state and update the current screen
                        self.reset_game()
                        self._current_screen = "Defult"
                except:
                    pass
        for button in self._buttons:
            button.check_for_click(
                filter(lambda event: event.type == pygame.MOUSEBUTTONUP, event_list))

    def handle_input(self):
        pass

    def draw(self, ui: UiBuilder, text_wrapper: WrapText):
        
        if self._current_screen == "Defult":
            self.Defult_Screen(ui)
        if self._current_screen == "Main_Game":
            self.Main_Game(ui)
        if self._current_screen == "After_Game":
            self.After_Game(ui)

        for button in self._buttons:
            button.draw(self._game.surface)
