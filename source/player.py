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
    climb_speed = constants.PLAYER_CLIMB_SPEED

    image = None
    level = None

    # Methods
    def __init__(self):

        # Constructor

        # Call parents constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = spritesheet.SpriteSheet("resources/player.png")

        # Get the standing image
        self.stand_image_r = sprite_sheet.get_image(0, 0, 24, 48)
        self.stand_image_l = pygame.transform.flip(self.stand_image_r, True, False)

        # Get the crouching image
        self.crouch_image_r = sprite_sheet.get_image(96, 0, 48, 24)
        self.crouch_image_l = pygame.transform.flip(self.crouch_image_r, True, False)

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

        # Get the crouching animation
        self.crouching_frames_r = []
        self.crouching_frames_l = []

        self.crouching_frames_r.append(self.crouch_image_r)
        image = sprite_sheet.get_image(96, 24, 48, 24)
        self.crouching_frames_r.append(image)

        # Flip them
        for frame in self.crouching_frames_r:
            image = pygame.transform.flip(frame, True, False)
            self.crouching_frames_l.append(image)

        # Get the dissolve animation
        self.dissolve_frames_r = []
        self.dissolve_frames_l = []

        image = sprite_sheet.get_image(0, 48, 22, 48)
        self.dissolve_frames_r.append(image)
        image = sprite_sheet.get_image(22, 48, 20, 46)
        self.dissolve_frames_r.append(image)
        image = sprite_sheet.get_image(42, 48, 16, 34)
        self.dissolve_frames_r.append(image)
        image = sprite_sheet.get_image(58, 48, 14, 24)
        self.dissolve_frames_r.append(image)
        image = sprite_sheet.get_image(72, 48, 10, 14)
        self.dissolve_frames_r.append(image)
        image = sprite_sheet.get_image(82, 48, 6, 10)
        self.dissolve_frames_r.append(image)

        # Flip them
        for frame in self.dissolve_frames_r:
            image = pygame.transform.flip(frame, True, False)
            self.dissolve_frames_l.append(image)

        # Create an empty image for when the player needs to be hidden
        self.empty_image = sprite_sheet.get_image(88, 48, 4, 4)

        # Set the starting image
        self.image = self.stand_image_r

        # Set a reference to the image rectangle
        self.rect = self.image.get_rect()

        # Create a hitmask
        self.hitmask_stand = funcs.create_mask(self.stand_image_r)
        self.hitmask_crouch = funcs.create_mask(self.crouch_image_r)

        self.hitmask = self.hitmask_stand

        self.footstep = pygame.mixer.Sound("resources/step.wav")
        self.footstep.set_volume(0.5)

        self.fall = pygame.mixer.Sound("resources/fall.wav")
        self.fall.set_volume(0.5)

        self.walk_dist = 0

        # The players stats
        self.health = 100
        self.stamina = 100

        # Vars for controlling what the player is doing

        self.climbing = False
        self.touching_ladder = False

        self.crouching = False

        self.in_air = False
        self.air_time = 0

        self.dying = False
        self.death_progress = 0

    def update(self):

        if self.dying:
            self.death_progress += 1

            if self.death_progress % 5 == 0 and self.death_progress < 30:
                old_center = self.rect.center
                if self.direction == "R":
                    self.image = self.dissolve_frames_r[int(self.death_progress/5)]
                else:
                    self.image = self.dissolve_frames_l[int(self.death_progress/5)]
                self.rect = self.image.get_rect()
                self.rect.center = old_center

            elif self.death_progress >= 30:
                self.image = self.empty_image

            return

        self.touching_ladder = self.on_ladder()

        if self.crouching:

            if self.direction == "R":
                self.image = self.crouch_image_r
            else:
                self.image = self.crouch_image_l

        # Calculate gravity
        if self.yv == 0:
            self.yv = 1
        elif self.touching_ladder and not self.climbing:
            self.yv = self.climb_speed
        else:
            self.yv += self.gravity

            if self.yv >= 15:
                self.yv = 15

        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.yv >= 0:
            self.yv = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

        # Momentum
        self.xv *= self.friction
        if abs(self.xv) <= 0.1:
            self.xv = 0
            self.walk_dist = 0
        else:
            self.walk_dist += 1
            self.stamina -= 0.008

        # Move left/right
        self.rect.x += self.xv

        if self.crouching:
            if self.xv != 0:
                if self.direction == "R":
                    frame = self.walk_dist // 7 % len(self.crouching_frames_r)
                    self.image = self.crouching_frames_r[frame]
                else:
                    frame = self.walk_dist // 7 % len(self.crouching_frames_l)
                    self.image = self.crouching_frames_l[frame]
        else:
            if self.direction == "R":
                frame = self.walk_dist // 7 % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            else:
                frame = self.walk_dist // 7 % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]

        if int(self.walk_dist) % 20 == 0 and not self.walk_dist == 0 and self.on_ground():
            pygame.mixer.Sound.play(self.footstep)

        if self.xv == 0 and not self.crouching:
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

        if not (self.on_ground() or self.on_ladder()):
            self.in_air = True

        if (self.on_ground() or self.on_ladder()) and self.in_air:
            if self.air_time > 45:
                self.fall.play()
                self.health -= self.air_time / 7.5
            self.in_air = False
            self.air_time = 0

        if self.in_air:
            self.air_time += 1

        # Player slowly regains health and stamina
        if self.health < 100:
            self.health += 0.001

        if self.stamina < 100:
            self.stamina += 0.004

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
        self.xv += (self.speed / 1.5) * ((self.stamina / 400) + 0.75) \
            if self.crouching or self.climbing else self.speed * ((self.stamina / 400) + 0.75)
        self.direction = "R"

    def walk_left(self):

        # Moves the player left
        self.xv -= (self.speed / 2) * ((self.stamina / 400) + 0.75) \
            if self.crouching or self.climbing else self.speed * ((self.stamina / 400) + 0.75)
        self.direction = "L"

    def jump(self):

        if self.touching_ladder:

            self.yv = -self.climb_speed
            self.climbing = True

        elif self.on_ground():

            self.yv = -self.jump_height

    def reset(self):

        # Reset to the sprites original position and image
        self.image = self.stand_image_r
        self.rect = self.image.get_rect()
        self.rect.x = 48
        self.rect.y = 385
        self.xv = 0
        self.yv = 0
        self.direction = "R"
        self.dying = False
        self.death_progress = 0
        self.in_air = False
        self.air_time = 0

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

    def on_ladder(self):

        # Check if the player is touching a ladder
        ladder_hit_list = pygame.sprite.spritecollide(self, self.level.ladders, False)

        return True if len(ladder_hit_list) else False

    def at_wall(self, direction):

        # Checks if the player is at a wall

        self.rect.x += 24 * direction
        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.x -= 24 * direction

        return True if len(hit_list) else False

    def do_crouch(self):

        at_wall_l = False
        at_wall_r = False

        # Function to make the player crouch
        if self.on_ground() and not self.climbing:

            # Check the player isn't at a wall
            if self.direction == "R":
                at_wall_r = self.at_wall(1)
            else:
                at_wall_l = self.at_wall(-1)

            if not(at_wall_l or at_wall_r):
                self.crouching = True

                if self.rect.height == 48:
                    self.rect.height = 24
                    self.rect.width = 48
                    self.rect.y += 24

                    if self.direction == "L":
                        self.rect.x -= 24

                    self.hitmask = self.hitmask_crouch

    def stop_crouching(self):

        if self.can_stand():
            if self.rect.height == 24:
                self.crouching = False
                self.rect.width = 24
                self.rect.height = 48
                self.rect.y -= 24

                if self.direction == "L":
                    self.rect.x += 24

                self.hitmask = self.hitmask_stand

    def can_stand(self):

        # This checks if there is a roof directly above the player
        self.rect.y -= 24
        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y += 24

        return False if len(hit_list) else True
