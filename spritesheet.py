import pygame


class SpriteSheet(object):

    sprite_sheet = None

    def __init__(self, filename):

        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):

        # Create a new blank image
        image = pygame.Surface([width, height], flags=pygame.SRCALPHA)
        image = image.convert_alpha()

        # Copy the sprite from the sprite sheet
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))

        # Return the image
        return image
