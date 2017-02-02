import pygame
import spritesheet
import math


class Arm(pygame.sprite.Sprite):

    sprite_sheet = None

    guard = None

    def __init__(self):

        # Constructor
        pygame.sprite.Sprite.__init__(self)

        # Load the image
        self.sprite_sheet = spritesheet.SpriteSheet("resources/arms.png")

        self.arm_right = self.sprite_sheet.get_image(0, 0, 28, 12)
        self.arm_left = self.sprite_sheet.get_image(0, 12, 28, 12)

        self.image = self.arm_right

        # Set a reference to the images rectangle
        self.rect = self.image.get_rect()

    def update(self):

        if self.guard.direction == "R":
            self.rect.x = self.guard.rect.x + self.guard.rect.width / 4
        else:
            self.rect.x = self.guard.rect.x + self.guard.rect.width * 0.6
        self.rect.y = self.guard.rect.y + self.guard.rect.height / 4

        if self.guard.direction == "R":
            self.image = self.arm_right
        else:
            self.image = self.arm_left

        # Calculate the angle at which to point at

        dx = self.guard.rect.x - self.guard.player.rect.x
        dy = self.guard.rect.y - self.guard.player.rect.y

        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        degrees = math.degrees(rads)
        print(degrees)
