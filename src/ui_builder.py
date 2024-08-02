import pygame
from player import Player


class UiBuilder:
    """
    This is the menu builder class

    this class takes the window height and width along with the window
    we then create local instances of each of these to use in the building of these screens

    """

    font_filepath = "assets/hf-free-complete/matchup-pro-v1.1/MatchupPro.otf"

    def __init__(self, window, height, width):
        self.window = window
        self.height = height
        self.width = width

    def draw_title(self, text, color):
        self.issue_font = pygame.font.Font(self.font_filepath, 50)
        title_text = self.issue_font.render(text, True, color)
        self.window.blit(title_text, ((self.width/2) - title_text.get_width() /
                                      2, title_text.get_height()/2))
    # Here we can create the title we pass through the color and text this will display the text on the top of the window
    # it will also be larger text but the positing is constant

    def set_background(self, loaded_img):
        self.window.blit(pygame.transform.scale(
            loaded_img, (self.width, self.height)), (0, 0))
    # set background takes a loaded image and scales it to the size of the window and sets it as the background
    # It is important to remember that if you call the background after displaying text or image it will hide these elements

    def draw_basic_text(self, text, color, font_size, x_pos, y_pos):
        main_font = pygame.font.Font(self.font_filepath, font_size)
        main_text = main_font.render(text, True, color)
        button = pygame.Rect(
            x_pos, y_pos, main_text.get_width(), main_text.get_height())
            
        # wrap text functionality
        # split the individual words from a text file and put them in a 2D array of lines of words 
        words = text.split()
        lines = []
        while len(words) > 0:
            # get as many words as will fit within the width of the textbox for each line of text
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                window_width, window_height = main_font.size(' '.join(line_words + words[:1])) # set height and width of text box
                if window_width > 1000: # if line is longer than width of box, start new line
                    break
            # append lines to array
            line = ' '.join(line_words)
            lines.append(line)
        # render the text on the screen
        distance = 0
        for line in lines:
            window_width, window_height = main_font.size(line)
            font_surface = main_font.render(line, True, color)
            self.window.blit(font_surface, (x_pos, y_pos + distance))
            distance += window_height + 20  # distance between each line, update after each line is rendered

        return button
    
        """
        This is used to display any basic text in any position

        We take the text to display as a string
        The color is a touple of rgb
        The font type is a string 
        the font size is a int
        the x and y pos is a int 

        these types are same for each of these functions 

        we return the button no matter what but isnt needed to use it
        """

    def draw_centered_basic_text(self, text, color, font_size, y_pos):
        main_font = pygame.font.Font(self.font_filepath, font_size)
        main_text = main_font.render(text, True, color)
        button = pygame.Rect((self.width/2 - main_text.get_width()),
                             y_pos, main_text.get_width()*2, main_text.get_height())

        self.window.blit(main_text, ((self.width/2) - main_text.get_width() /
                                     2, (y_pos - main_text.get_height()/2)))
        return button

    # this is the same as the last function but instead the text is centered to the screen and adjusted by the size the text takes up

    def place_image(self, loaded_img, translated_width, translated_height, x_pos, y_pos):
        self.window.blit(pygame.transform.scale(
            loaded_img, (translated_width, translated_height)), (x_pos, y_pos))
        button = pygame.Rect(x_pos, y_pos, translated_width, translated_height)
        return button
    # thsi is used to place a image at a position on the screen along with this it adjusts the hight and width of the image to what you want
    # also returns a button of the size of the image

    def draw_rect(self, x_pos, y_pos, width, height, color):
        input_rect = pygame.Rect(x_pos, y_pos, width, height)
        pygame.draw.rect(self.window, color, input_rect)

    def draw_top_bar(self, player: Player):
        self.draw_rect(0, 0, self.width, 125, (128, 128, 128))
        self.draw_basic_text("Balance: {}".format(
            player.balance), (255, 255, 255), 30, ((self.width+30) - self.width), 30)


    def Display_cards(self, hand, pos, turn, doubled=0):
        hand_size = len(hand)
        i = 0
        if turn == "dealer":
            while i < hand_size:
                x_pos = pos[0] - (50 * i)
                y_pos = pos[1] + (50 * i)
                card = hand[i]
                card.draw(4.0, self.window, x_pos, y_pos)
                
                i += 1
        else:
            if doubled != 0:
                while i < hand_size:
                    x_pos = pos[0] + (50 * i)
                    y_pos = pos[1] - (50 * i)
                    card = hand[i]
                    if i == 2:
                        card.draw(4.0, self.window, x_pos, y_pos, 90)
                    else:
                        card.draw(4.0, self.window, x_pos, y_pos)
                    i += 1
            else:
                while i < hand_size:
                    x_pos = pos[0] + (50 * i)
                    y_pos = pos[1] - (50 * i)
                    card = hand[i]
                    card.draw(4.0, self.window, x_pos, y_pos)
                    i += 1

    def Delay_Display_cards(self, hand, pos):
        hand_size = len(hand)
        i = 0
        while i < hand_size:
            if i < 2:
                x_pos = pos[0] - (50 * i)
                y_pos = pos[1] + (50 * i)
                card = hand[i]
                card.draw(4.0, self.window, x_pos, y_pos)
                pygame.display.update()
                i += 1
            else:
                x_pos = pos[0] - (50 * i)
                y_pos = pos[1] + (50 * i)
                card = hand[i]
                pygame.time.delay(1000)
                card.draw(4.0, self.window, x_pos, y_pos)
                pygame.display.update()
                i += 1
            

    def Back_Card(self, card):
        card.is_face_up = False

    def Front_Card(self, card):
        card.is_face_up = True
