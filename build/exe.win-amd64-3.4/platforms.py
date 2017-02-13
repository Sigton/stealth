import pygame
import spritesheet

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
LAMP = (120, 48, 24, 24)
CHAIN = (144, 48, 24, 24)
ACID_TOP = (
    (168, 48, 24, 24),
    (168, 72, 24, 24)
)
ACID = (144, 72, 24, 24)
LADDER = (120, 72, 24, 24)

platforms = (
    GROUND1, GROUND2, GROUND3, GROUND4, GROUND5,
    GROUND6, GROUND7, GROUND8, GROUND9, GROUND10,
    GROUND11, GROUND12, GROUND13, GROUND14, GROUND15,
    GROUND16, CRATE, GIRDER1, GIRDER2, GIRDER3,
    LAMP, CHAIN, ACID_TOP, ACID, LADDER
)


class Platform(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet_data):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = spritesheet.SpriteSheet("resources/terrain.png")

        self.image = sprite_sheet.get_image_srcalpha(sprite_sheet_data[0],
                                                     sprite_sheet_data[1],
                                                     sprite_sheet_data[2],
                                                     sprite_sheet_data[3])

        self.rect = self.image.get_rect()


class AnimatedPlatform(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet_data):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/terrain.png")

        self.images = []

        # Take the image for each frame from the spritesheet
        # And add it to the list of frames

        for sprite in sprite_sheet_data:
            new_image = self.sprite_sheet.get_image_srcalpha(sprite[0],
                                                             sprite[1],
                                                             sprite[2],
                                                             sprite[3])
            self.images.append(new_image)

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # A timer var for animation

        self.tick = 0
        self.frame = 0

    def update(self):

        self.tick += 1

        if self.tick % 10 == 0:
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]
