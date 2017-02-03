import pygame
try:
    import spritesheet
except ImportError:
    from source import *

GROUND1 = (0, 0, 24, 24)
GROUND2 = (24, 0, 24, 24)
GROUND3 = (48, 0, 24, 24)
GROUND4 = (72, 0, 24, 24)
GROUND5 = (96, 0, 24, 24)
GROUND6 = (120, 0, 24, 24)
GROUND7 = (144, 0, 24, 24)
GROUND8 = (168, 0, 24, 24)
GROUND9 = (0, 24, 24, 24)
GROUND10 = (24, 24, 24, 24)
GROUND11 = (48, 24, 24, 24)
GROUND12 = (72, 24, 24, 24)
GROUND13 = (96, 24, 24, 24)
GROUND14 = (120, 24, 24, 24)
GROUND15 = (144, 24, 24, 24)
GROUND16 = (168, 24, 24, 24)
CRATE = (0, 48, 24, 24)
GIRDER1 = (24, 48, 24, 24)
GIRDER2 = (48, 48, 24, 24)
GIRDER3 = (72, 48, 24, 24)

platforms = (
    GROUND1, GROUND2, GROUND3, GROUND4, GROUND5,
    GROUND6, GROUND7, GROUND8, GROUND9, GROUND10,
    GROUND11, GROUND12, GROUND13, GROUND14, GROUND15,
    GROUND16, CRATE, GIRDER1, GIRDER2, GIRDER3
)


class Platform(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet_data):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = spritesheet.SpriteSheet("resources/terrain.png")

        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()