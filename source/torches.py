import pygame

import spritesheet
import funcs


class Torch(pygame.sprite.Sprite):

    direction = "R"

    guard = None

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the image
        self.sprite_sheet = spritesheet.SpriteSheet("resources/light.png")
        self.image_r = self.sprite_sheet.get_image_srcalpha(0, 0, 160, 94)
        self.image_l = self.sprite_sheet.get_image_srcalpha(0, 94, 160, 94)

        self.image = self.image_r

        # Set the position
        self.rect = self.image.get_rect()

        # Create a hitmask
        self.hitmask_r = funcs.create_mask(self.image_r)
        self.hitmask_l = funcs.create_mask(self.image_l)

        self.hitmask = self.hitmask_r

    def update(self):

        # Move to guards position
        self.direction = self.guard.direction

        if self.direction == "R":
            self.image = self.image_r
            self.rect.x = self.guard.rect.x + self.guard.rect.width / 2
            self.hitmask = self.hitmask_r
        else:
            self.image = self.image_l
            self.rect.x = (self.guard.rect.x + self.guard.rect.width / 2) - self.rect.width
            self.hitmask = self.hitmask_l

        self.rect.y = self.guard.rect.y - self.guard.rect.height / 2
