import csv
from spritesheet import Spritesheet


class Texture:
    def __init__(self, images: str, coordinates_file: str):
        """Args:
            images: file location of the image from which to pull the rectangles
            coordinates_file: file location of the CSV file containing x and y 
                              coordinates of the rectangles within the spritesheet
        """
        self.images = Spritesheet(images)
        self.coordinates = {}
        with open(coordinates_file) as input_file:
            reader = csv.reader(input_file)
            # skip the header row
            next(reader, None)
            for row in reader:
                self.coordinates[row[0]] = (row[1], row[2])
