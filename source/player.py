import pygame

import spritesheet
import constants
import funcs


class Player(pygame.sprite.Sprite):

    # Attributes
    xv = 0
    yv = 0

    direction = "R"

    speed = constants.PLAYER_SPEED
    gravity = constants.PLAYER_GRAVITY
    friction = constants.PLAYER_FRICTION
    jump_height = constants.PLAYER_JUMP_HEIGHT

    image = None
    level = None
    health_bar = None  # tbc

    # Methods
    def __init__(self):

        # Constructor

        # Call parents constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = spritesheet.SpriteSheet("resources/player.png")

        # Get the standing image
        self.stand_image_r = sprite_sheet.get_image(0, 0, 24, 48)
        self.stand_image_l = pygame.transform.flip(self.stand_image_r, True, False)

        # Arrays for animation
        self.walking_frames_r = []
        self.walking_frames_l = []

        # Load the images
        image = sprite_sheet.get_image(0, 0, 24, 48)
        self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(24, 0, 24, 48)
        self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(48, 0, 24, 48)
        self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(72, 0, 24, 48)
        self.walking_frames_r.append(image)

        # Flip them to the left
        for frame in self.walking_frames_r:
            image = pygame.transform.flip(frame, True, False)
            self.walking_frames_l.append(image)

        # Set the starting image
        self.image = self.stand_image_r

        # Set a reference to the image rectangle
        self.rect = self.image.get_rect()

        # Create a hitmask
        self.hitmask = funcs.create_mask(self.image)

        self.footstep = pygame.mixer.Sound("resources/step.wav")
        self.footstep.set_volume(0.5)

        self.walk_dist = 0

    def update(self):

        # Calculate gravity
        if self.yv == 0:
            self.yv = 1
        else:
            self.yv += self.gravity

        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.yv >= 0:
            self.yv = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

        # Momentum
        self.xv *= self.friction
        if abs(self.xv) <= 0.5:
            self.xv = 0
            self.walk_dist = 0
        else:
            self.walk_dist += 1

        # Move left/right
        self.rect.x += self.xv

        if self.direction == "R":
            frame = self.walk_dist // 10 % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = self.walk_dist // 10 % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        if int(self.walk_dist) % 20 == 0 and not self.walk_dist == 0 and self.on_ground():
            pygame.mixer.Sound.play(self.footstep)

        if self.xv == 0:
            if self.direction == "R":
                self.image = self.stand_image_r
            else:
                self.image = self.stand_image_l

        # Check for collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.xv > 0:
                self.rect.right = block.rect.left
            elif self.xv < 0:
                self.rect.left = block.rect.right
            self.walk_dist = 0

        # So the player can't walk off the left side of the screen
        if self.rect.x <= 0:
            self.rect.x = 0
            self.xv = 0
            self.walk_dist = 0

        # Move up/down
        self.rect.y += self.yv

        # Check for collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.yv > 0:
                self.rect.bottom = block.rect.top
            elif self.yv < 0:
                self.rect.top = block.rect.bottom

            # Stop vertical movement
            self.yv = 0

        # So the player can't jump off the top of the screen
        if self.rect.y + self.rect.height <= 0:
            self.rect.y = 0 - self.rect.height
            self.yv = 0

    def on_ground(self):

        # Helper function that returns whether the player is on the ground
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) or self.rect.bottom > constants.SCREEN_HEIGHT:
            return True
        else:
            return False

    def walk_right(self):

        # Moves the player right
        self.xv += self.speed
        self.direction = "R"

    def walk_left(self):

        # Moves the player left
        self.xv -= self.speed
        self.direction = "L"

    def jump(self):

        if self.on_ground():
            self.yv = -self.jump_height

    def reset(self):

        # Reset to the sprites original position and image
        self.rect.x = 48
        self.rect.y = 624
        self.xv = 0
        self.yv = 0
        self.direction = "R"
        self.image = self.stand_image_r

    def use_keypad(self):

        # If the player is touching the keypad, increase the progress
        touching_keypads = pygame.sprite.spritecollide(self, self.level.keypads, False)
        for keypad in touching_keypads:
            if keypad.progress < 10:
                keypad.progress += 1

        # Bombs too
        touching_bombs = pygame.sprite.spritecollide(self, self.level.bombs, False)
        for bomb in touching_bombs:
            if bomb.progress < 10:
                bomb.progress += 1
