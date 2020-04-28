import pygame
from src import constants


class SpriteSheet(object):

    sprite_sheet = None

    def __init__(self, filename):

        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):

        # Create a blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the sprite sheet
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Set white to transparent
        image.set_colorkey(constants.WHITE)

        # Return the image
        return image

    def get_image_srcalpha(self, x, y, width, height):

        # Create a new blank image
        image = pygame.Surface([width, height], flags=pygame.SRCALPHA)
        image = image.convert_alpha()

        # Copy the sprite from the sprite sheet
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))

        # Return the image
        return image


# Used to blit an image at a certain opacity
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)
