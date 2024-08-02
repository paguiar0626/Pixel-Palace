import pygame

""" class to read from text file"""
class ReadInstructions:

    # read the text file and save the contents
    def __init__(self, file_name):
        file = open(file_name, "r")
        self.contents = file.read()
        file.close()

    # return the text
    def get_contents(self):
        return self.contents
    

""" class to wrap the text around the window so it doesn't go offscreen in the instructions menus"""
class WrapText:

    font_filepath = "assets/hf-free-complete/matchup-pro-v1.1/MatchupPro.otf"

    # set variables for the window size
    def __init__(self, window, height, width):
        self.window = window
        self.height = height
        self.width = width

    # Wrap text around the screen by breaking up the lines of text
    def make_lines(self, text, main_font):
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
        # return the lines of text
        return lines

    # render the text on screen
    def draw_wrapped_text(self, text, color, font_size, x_pos, y_pos):
        # initialize text
        main_font = pygame.font.Font(self.font_filepath, font_size)
        main_text = main_font.render(text, True, color)
        button = pygame.Rect(x_pos, y_pos, main_text.get_width(), main_text.get_height())

        # render the text
        lines = self.make_lines(text, main_font)
        distance = 50 
        for line in lines:
            window_width, window_height = main_font.size(line)
            font_surface = main_font.render(line, True, color)
            self.window.blit(font_surface, (x_pos, y_pos + distance))
            distance += window_height + 25  # distance between each line, update after each line is rendered

        return button
