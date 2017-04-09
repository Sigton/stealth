import pygame

import spritesheet
import torches
import guard_parts
import constants
import math


class Guard(pygame.sprite.Sprite):

    # Attributes

    xv = 0
    direction = "R"

    speed = constants.GUARD_SPEED

    player = None
    level = None
    torch = None

    sprite_sheet = None

    def __init__(self, x, y):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/guard.png")

        # Get the standing images
        self.stand_image_r = self.sprite_sheet.get_image_srcalpha(0, 0, 24, 48)
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
        self.rect.x = x
        self.rect.y = y

        self.start_x = x
        self.start_y = y

        self.torch = torches.Torch()
        self.torch.guard = self
        self.torch.start_x = self.start_x + self.rect.width / 2
        self.torch.start_y = self.start_y + self.rect.height / 2

        # Var for animation
        self.walk_dist = 0

    def update(self):

        # Update the position of the guards
        if not self.on_edge():
            if self.direction == "R":
                self.xv = self.speed
            else:
                self.xv = -self.speed
            self.rect.x += self.xv
            self.walk_dist += 1

        if self.at_wall() or self.on_edge():
            if self.direction == "R":
                self.direction = "L"
            else:
                self.direction = "R"

        if self.direction == "R":
            frame = (self.walk_dist // 12) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (self.walk_dist // 12) % len(self.walking_frames_l)
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


class HostileGuard(pygame.sprite.Sprite):

    xv = 0
    direction = "R"

    speed = constants.HGUARD_SPEED
    follow_dist = constants.HGUARD_FOLLOW_DIST

    player = None
    level = None
    arm = None

    sprite_sheet = None

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/hguard.png")

        self.stand_img_r = self.sprite_sheet.get_image(0, 0, 24, 48)
        self.stand_img_l = pygame.transform.flip(self.stand_img_r, True, False)

        self.walking_frames_r = []
        self.walking_frames_l = []

        image = self.sprite_sheet.get_image(0, 0, 24, 48)
        self.walking_frames_r.append(image)
        image = self.sprite_sheet.get_image(24, 0, 24, 48)
        self.walking_frames_r.append(image)
        image = self.sprite_sheet.get_image(48, 0, 24, 48)
        self.walking_frames_r.append(image)
        image = self.sprite_sheet.get_image(72, 0, 24, 48)
        self.walking_frames_r.append(image)

        for frame in self.walking_frames_r:
            image = pygame.transform.flip(frame, True, False)
            self.walking_frames_l.append(image)

        self.image = self.stand_img_r

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start_x = x
        self.start_y = y

        self.arm = guard_parts.Arm(self)

    def update(self):

        if self.rect.x < self.player.rect.x:
            self.direction = "R"
        else:
            self.direction = "L"

        if self.dist_to(self.player.rect.x, self.player.rect.y) < self.follow_dist and not self.on_edge():
            if self.direction == "R":
                self.xv = self.speed
            else:
                self.xv = -self.speed / 2

        if not abs(self.player.rect.x - self.rect.x) <= 5:
            if not self.at_wall():
                self.rect.x += self.xv
                self.xv *= constants.HGUARD_FRICTION
                if abs(self.xv) <= 0.5:
                    self.xv = 0

                block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
                for block in block_hit_list:
                    if self.xv > 0:
                        self.rect.right = block.rect.left
                    else:
                        self.rect.left = block.rect.right
                    self.xv = 0
            else:
                self.xv = 0

        else:
            self.xv = 0

        if abs(self.xv) > 0.5:
            if self.direction == "R":
                frame = (self.rect.x // 15) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            else:
                frame = (self.rect.x // 15) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]
        else:
            if self.direction == "R":
                self.image = self.stand_img_r
            else:
                self.image = self.stand_img_l

    def dist_to(self, x, y):

        dx = x - self.rect.x
        dy = y - self.rect.y

        dist = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
        return dist

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
