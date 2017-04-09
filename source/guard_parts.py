import pygame
import spritesheet
import math


class Arm(pygame.sprite.Sprite):

    sprite_sheet = None

    guard = None

    def __init__(self, guard):

        # Constructor
        pygame.sprite.Sprite.__init__(self)

        # Load the image
        self.sprite_sheet = spritesheet.SpriteSheet("resources/arms.png")

        self.arm_right = self.sprite_sheet.get_image(0, 0, 28, 12)
        self.arm_left = self.sprite_sheet.get_image(0, 12, 28, 12)

        self.image = self.arm_right

        self.guard = guard

        # Set a reference to the images rectangle
        self.rect = self.image.get_rect()

        self.rect.x = self.guard.rect.x + self.guard.rect.width / 4
        self.rect.y = self.guard.rect.y + self.guard.rect.height / 4

        self.start_x = self.rect.x
        self.start_y = self.rect.y

    def update(self):

        if self.guard.direction == "R":
            self.rect.x = self.guard.rect.x + self.guard.rect.width / 4
        else:
            self.rect.x = self.guard.rect.x + self.guard.rect.width * -0.4
        self.rect.y = self.guard.rect.y + self.guard.rect.height / 4

        if self.guard.direction == "R":
            self.image = self.arm_right
        else:
            self.image = self.arm_left

        # Calculate the angle at which to point at

        dx = self.guard.rect.x - self.guard.player.rect.x
        dy = self.guard.rect.y - self.guard.player.rect.y

        # Gotta love trig
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        degrees = math.degrees(rads)
        degrees = (degrees + 180) % 360

        # Rotate the image and reset the rect
        self.image = pygame.transform.rotate(self.image, degrees)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Align rectangle after rotation
        if degrees > 180:
            self.rect.top = self.guard.rect.y + (self.guard.rect.height * 0.25)
        else:
            self.rect.bottom = self.guard.rect.y + (self.guard.rect.height * 0.5)
        if self.guard.direction == "R":
            self.rect.left = self.guard.rect.left + self.guard.rect.width * 0.2
        else:
            self.rect.right = self.guard.rect.right - self.guard.rect.width * 0.2


class Bullet(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
