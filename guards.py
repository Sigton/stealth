import pygame
import spritesheet
import torches
import constants


class Guard(pygame.sprite.Sprite):

    # Attributes

    xv = 0
    direction = "R"

    speed = constants.GUARD_SPEED

    player = None
    level = None
    torch = None

    sprite_sheet = None

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/guard.png")

        # Get the standing images
        self.stand_image_r = self.sprite_sheet.get_image(0, 0, 24, 48)
        self.stand_image_l = pygame.transform.flip(self.stand_image_r, True, False)

        # Arrays for animation
        self.walking_frames_r = []
        self.walking_frames_l = []

        # Load the images
        image = self.sprite_sheet.get_image(0, 0, 24, 48)
        self.walking_frames_r.append(image)

        image = self.sprite_sheet.get_image(24, 0, 25, 48)
        self.walking_frames_r.append(image)

        image = self.sprite_sheet.get_image(48, 0, 24, 48)
        self.walking_frames_r.append(image)

        image = self.sprite_sheet.get_image(72, 0, 24, 48)
        self.walking_frames_r.append(image)

        # Flip them
        for image in self.walking_frames_r:
            self.walking_frames_l.append(pygame.transform.flip(image, True, False))

        # Set the starting image and rect
        self.image = self.stand_image_r

        self.rect = self.image.get_rect()

        self.torch = torches.Torch()
        self.torch.guard = self

    def update(self):

        # Update the position of the guards
        if not self.on_edge():
            if self.direction == "R":
                self.xv = self.speed
            else:
                self.xv = -self.speed/2  # For some reason guards move twice as fast left

            self.rect.x += self.xv

        if self.at_wall() or self.on_edge():
            if self.direction == "R":
                self.direction = "L"
            else:
                self.direction = "R"

        if self.direction == "R":
            frame = (self.rect.x // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (self.rect.x // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

    def on_ground(self):

        # Helper function to check if sprite is on the ground
        self.rect.y += 2
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(block_hit_list):
            return True
        else:
            return False

    def on_edge(self):

        # Helper function that checks if sprite is on an edge

        if self.direction == "R":

            self.rect.x += 24
            on_ground = self.on_ground()
            self.rect.x -= 24

            if on_ground:
                return False
            else:
                return True

        else:

            self.rect.x -= 24
            on_ground = self.on_ground()
            self.rect.x += 24

            if on_ground:
                return False
            else:
                return True

    def at_wall(self):

        if self.direction == "R":

            self.rect.x += 24
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            self.rect.x -= 24

            if len(block_hit_list):
                return True
            else:
                return False

        else:

            self.rect.x -= 24
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            self.rect.x += 24

            if len(block_hit_list):
                return True
            else:
                return False
